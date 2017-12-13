import hashlib
from decimal import Decimal
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import AccessMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from carton.cart import Cart
from shoping.apps.product.models import Product
from shoping.apps.ticket.models import Ticket, Status
from shoping.apps.epayco.models import EpayCo
from shoping.apps.core.tasks import task_sendgrid_mail
from django.contrib import messages

class ProductListView(ListView):
    model = Product

class ProductDetailView(DetailView):
    model = Product

class TicketDetailView(LoginRequiredMixin, DetailView):
    template_name = 'shop/ticket.html'
    model = Ticket

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class EpaycoView(AccessMixin, DetailView):
    """
    METHOD GET GENERATE FORM EPAYCO
    METHOD POST RESPONSE EPAYCO
    """

    template_name = {
        'GET': 'shop/epayco.html',
        'POST': 'shop/ticket.html'
    }

    http_method_names = ('get', 'post', )

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if (request.is_ajax()
                and request.method == 'POST'
                or request.user.is_authenticated):
            # no valida auth si el request viene por POST AJAX
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


    def get_login_url(self):
        if self.login_url:
            return super().get_login_url()
        return '{}?{}={}'.format(
            reverse('login'),
            self.redirect_field_name,
            self.request.path
        )

    def get_template_names(self):
        self.template_name = self.template_name[self.request.method]
        return super().get_template_names()

    def get(self, request, *args, **kwargs):

        ticket = self.get_object()
        epayco = EpayCo.objects.first()

        if ticket is None:
            raise Http404

        p_description = 'demo-app-co ePayCo'
        p_cust_id_cliente = epayco.client_id
        p_key = epayco.p_key
        p_id_invoice = '{}'.format(ticket.pk)
        p_amount = '{}'.format(ticket.total)
        p_currency_code = epayco.p_currency_code

        signature = '{0}^{1}^{2}^{3}^{4}'.format(
            p_cust_id_cliente,
            p_key,
            p_id_invoice,
            p_amount,
            p_currency_code
        )

        h = hashlib.md5()
        h.update(signature.encode('utf-8'))
        p_signature = h.hexdigest()

        p_tax = 0
        p_amount_base = 0
        p_test_request = 'TRUE' if epayco.test else 'FALSE'

        p_url_response = epayco.url_response
        p_url_confirmation = epayco.url_confirmation

        context = {
            'p_cust_id_cliente': p_cust_id_cliente,
            'p_key': p_key,
            'p_id_invoice': p_id_invoice,
            'p_amount': p_amount,
            'p_currency_code': p_currency_code,
            'p_signature': p_signature,
            'p_tax': p_tax,
            'p_amount_base': p_amount_base,
            'p_test_request': p_test_request,
            'p_url_response': p_url_response,
            'p_url_confirmation': p_url_confirmation,
            'p_description': p_description
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        epayco = EpayCo.objects.first()
        x_signature = request.POST.get('x_signature')

        x_cust_id_cliente = request.POST.get('x_cust_id_cliente')
        x_key = epayco.p_key
        x_id_invoice = request.POST.get('x_id_invoice')
        x_ref_payco = request.POST.get('x_ref_payco')
        x_transaction_id = request.POST.get('x_transaction_id')
        x_amount = request.POST.get('x_amount')
        x_currency_code = request.POST.get('x_currency_code')

        x_cod_response = request.POST.get('x_cod_response')

        signature = '{0}^{1}^{2}^{3}^{4}^{5}'.format(
            x_cust_id_cliente,
            x_key,
            x_ref_payco,
            x_transaction_id,
            x_amount,
            x_currency_code
        )

        h = hashlib.sha256()
        h.update(signature.encode('utf-8'))
        v_signature = h.hexdigest()

        ticket = self.get_object(int(x_id_invoice))

        # ticket valido
        if (ticket and
                v_signature == x_signature and
                ticket.total == Decimal(x_amount)):

            ticket.status = Status(int(x_cod_response))
            if (ticket.status.pk in [
                    Status.REJECTE,
                    Status.FAILED]):
                messages.error(request, 'decline card.')
            else:
                messages.success(request, 'thanks for your purchase.')

        # ticket invalido
        else:
            if ticket:
                ticket.status = Status(Status.FAILED)
                messages.error(request, 'invalid ticket.')
            else:
                raise Http404

        # genera url y mail para notificar que el pedido a cambiado de estado
        next_url = request.build_absolute_uri(
            reverse('ticket_detail', args=[ticket.pk])
        )
        task_sendgrid_mail.delay('purchase',
            ticket.user.pk, ticket.pk, next_url=next_url)

        ticket.status = Status.objects.get(pk=ticket.status.pk)
        ticket.save()

        context = {'ticket': ticket}
        return self.render_to_response(context)

    def get_object(self, pk=None):
        if pk:
            return Ticket.objects.filter(pk=pk).first()
        else:
            cart = Cart(self.request.session)
            if cart.is_empty:
                return None
            ticket = Ticket()
            ticket.user = self.request.user
            ticket.total = cart.total
            ticket.status = Status(Status.PENDING)
            ticket.save()
            for item in cart.items:
                ticket.items.create(
                    product=item.product,
                    quantity=item.quantity
                )
            cart.clear()
        return ticket

class CartShowView(TemplateView):
    template_name = 'shop/cart_list.html'

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        delete = action == 'delete'
        clear = action == 'clear'

        cart = Cart(request.session)
        product = Product.objects.filter(pk=request.POST.get('product')).first()
        quantity = request.POST.get('quantity', 1)

        if delete:
            if cart.is_empty is False:
                cart.remove(product)
        elif clear:
            if cart.is_empty is False:
                cart.clear()
        else:
            cart.add(product, product.price, quantity)

        if cart.is_empty:
            return redirect('product_list')

        return super().get(request, *args, **kwargs)

