from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse

from .models import Customer, Ticket, Order, Seller
from .serializers import CustomerSerializer, TicketSerializer, OrderSerializer, SellerSerializer


#===== GETTING
# Отримати всіх продавців (MongoDB)
@api_view(['GET'])
def getSellers(request):
    sellers = Seller.objects.all()
    serializer = SellerSerializer(sellers, many=True)
    return Response(serializer.data)

# Отримати одного продавця (MongoDB)
@api_view(['GET'])
def getSeller(request, pk):
    try:
        seller = Seller.objects.get(id=pk)
        serializer = SellerSerializer(seller)
        return Response(serializer.data)
    except Seller.DoesNotExist:
        return Response({"error": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)

# Отримати всіх клієнтів (PostgreSQL)
@api_view(['GET'])
def getCustomers(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

# Отримати одного клієнта (PostgreSQL)
@api_view(['GET'])
def getCustomer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

# Отримати всі квитки (PostgreSQL)
@api_view(['GET'])
def getTickets(request):
    tickets = Ticket.objects.all()
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)

# Отримати один квиток (PostgreSQL)
@api_view(['GET'])
def getTicket(request, pk):
    try:
        ticket = Ticket.objects.get(id=pk)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

# Отримати всі замовлення (PostgreSQL)
@api_view(['GET'])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# Отримати одне замовлення (PostgreSQL)
@api_view(['GET'])
def getOrder(request, pk):
    try:
        order = Order.objects.get(id=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

#===== ADDING
# Створити нового продавця (MongoDB)
@api_view(['POST'])
def addSeller(request):
    serializer = SellerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Створити нового клієнта (PostgreSQL)
@api_view(['POST'])
def addCustomer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Створити новий квиток (PostgreSQL)
@api_view(['POST'])
def addTicket(request):
    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Створити нове замовлення (PostgreSQL)
@api_view(['POST'])
def addOrder(request):
    """
    Створити нове замовлення.
    Очікує структуру даних:
    {
        "customer": <ID клієнта>,
        "ticket": <ID квитка>,
        "seller": <ID продавця>
    }
    """
    serializer = OrderSerializer(data=request.data)

    # Перевірка валідності даних
    if serializer.is_valid():
        # Перевірка унікальності квитка
        ticket_id = serializer.validated_data['ticket'].id
        if Order.objects.filter(ticket_id=ticket_id).exists():
            return Response(
                {"error": "Цей квиток вже прив'язаний до існуючого замовлення."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Збереження замовлення
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#===== UPDATING
@api_view(['PUT'])
def updateOrder(request, pk):
    """
    Оновити існуюче замовлення.
    Очікує структуру даних:
    {
        "customer": <ID клієнта>,
        "ticket": <ID квитка>,
        "seller": <ID продавця>
    }
    """
    try:
        # Отримуємо замовлення за ID
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({"error": "Замовлення з вказаним ID не знайдено."}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order, data=request.data)

    if serializer.is_valid():
        # Перевірка, чи квиток прив'язаний до іншого замовлення
        new_ticket_id = serializer.validated_data['ticket'].id
        if Order.objects.filter(ticket_id=new_ticket_id).exclude(id=pk).exists():
            return Response(
                {"error": "Цей квиток вже прив'язаний до іншого замовлення."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Оновлення замовлення
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Customer
@api_view(['PUT'])
def updateCustomer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializer(customer, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Ticket
@api_view(['PUT'])
def updateTicket(request, pk):
    try:
        ticket = Ticket.objects.get(id=pk)
    except Ticket.DoesNotExist:
        return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = TicketSerializer(ticket, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Seller
@api_view(['PUT'])
def updateSeller(request, pk):
    try:
        seller = Seller.objects.get(id=pk)
    except Seller.DoesNotExist:
        return Response({"detail": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = SellerSerializer(seller, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE ONE
# Видалення одного клієнта
@api_view(['DELETE'])
def deleteCustomer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

    # Видалити всі замовлення, пов'язані з цим клієнтом
    deleted_orders = Order.objects.filter(customer=customer).delete()

    # Видалити самого клієнта
    customer.delete()
    return Response({
        "message": f"Customer and {deleted_orders[0]} related orders successfully deleted."
    }, status=status.HTTP_200_OK)

# Видалення одного квитка
@api_view(['DELETE'])
def deleteTicket(request, pk):
    try:
        ticket = Ticket.objects.get(id=pk)
    except Ticket.DoesNotExist:
        return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

    # Видалити всі замовлення, пов'язані з цим квитком
    deleted_orders = Order.objects.filter(ticket=ticket).delete()

    # Видалити сам квиток
    ticket.delete()
    return Response({
        "message": f"Ticket and {deleted_orders[0]} related orders successfully deleted."
    }, status=status.HTTP_200_OK)

# Видалення одного продавця
@api_view(['DELETE'])
def deleteSeller(request, pk):
    try:
        seller = Seller.objects.get(id=pk)
    except Seller.DoesNotExist:
        return Response({"detail": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)

    # Видалити всі замовлення, пов'язані з цим продавцем
    deleted_orders = Order.objects.filter(seller=seller).delete()

    # Видалити самого продавця
    seller.delete()
    return Response({
        "message": f"Seller and {deleted_orders[0]} related orders successfully deleted."
    }, status=status.HTTP_200_OK)

# Видалити одне замовлення
@api_view(['DELETE'])
def deleteOrder(request, pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    order.delete()
    return Response({"message": f"Order with ID {pk} successfully deleted."}, status=status.HTTP_200_OK)

# FILTER ORDERS
@api_view(['GET'])
def filterOrders(request):
    # Отримуємо параметри фільтрації з запиту
    seller_id = request.query_params.get('seller', None)
    start_date = request.query_params.get('start_date', None)
    end_date = request.query_params.get('end_date', None)

    orders = Order.objects.all()

    # Фільтрація за продавцем
    if seller_id:
        try:
            seller_id = int(seller_id)  # Перетворюємо на ціле число
            orders = orders.filter(seller_id=seller_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid seller ID'}, status=400)

    # Фільтрація за датою
    if start_date:
        start_date = parse_datetime(start_date)
        if not start_date:
            return JsonResponse({'error': 'Invalid start date format'}, status=400)
        orders = orders.filter(order_date__gte=start_date)

    if end_date:
        end_date = parse_datetime(end_date)
        if not end_date:
            return JsonResponse({'error': 'Invalid end date format'}, status=400)
        orders = orders.filter(order_date__lte=end_date)

    # Серіалізація та повернення результату
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# DELETE MANY
# Видалити багатьох клієнтів
# @api_view(['DELETE'])
# def deleteCustomers(request):
#     ids = request.data.get('ids', [])
#     if not ids:
#         return Response({"detail": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

#     deleted_count, _ = Customer.objects.filter(id__in=ids).delete()
#     return Response({"message": f"{deleted_count} customers successfully deleted."}, status=status.HTTP_200_OK)

# # Видалити багато квитків
# @api_view(['DELETE'])
# def deleteTickets(request):
#     ids = request.data.get('ids', [])
#     if not ids:
#         return Response({"detail": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

#     deleted_count, _ = Ticket.objects.filter(id__in=ids).delete()
#     return Response({"message": f"{deleted_count} tickets successfully deleted."}, status=status.HTTP_200_OK)

# # Видалити багатьох продавців
# @api_view(['DELETE'])
# def deleteSellers(request):
#     ids = request.data.get('ids', [])
#     if not ids:
#         return Response({"detail": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

#     deleted_count, _ = Seller.objects.filter(id__in=ids).delete()
#     return Response({"message": f"{deleted_count} sellers successfully deleted."}, status=status.HTTP_200_OK)

# # Видалити багато замовлень
# @api_view(['DELETE'])
# def deleteOrders(request):
#     ids = request.data.get('ids', [])
#     if not ids:
#         return Response({"detail": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

#     deleted_count, _ = Order.objects.filter(id__in=ids).delete()
#     return Response({"message": f"{deleted_count} orders successfully deleted."}, status=status.HTTP_200_OK)