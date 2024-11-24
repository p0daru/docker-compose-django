from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Customer, Ticket, Seller, Order
from .serializers import CustomerSerializer, TicketSerializer, SellerSerializer, OrderSerializer
from datetime import datetime

# Create your views here.

# Get all customers
@api_view(['GET'])
def getCustomers(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

# Get a single customer
@api_view(['GET'])
def getCustomer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
        serializer = CustomerSerializer(customer, many=False)
        return Response(serializer.data)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)

# Add customer
@api_view(['POST'])
def addCustomer(request):
    # Серіалізуємо всі передані дані (список користувачів)
    serializer = CustomerSerializer(data=request.data, many=True)
    
    if serializer.is_valid():
        # Створюємо кілька користувачів за раз
        Customer.objects.bulk_create([Customer(**item) for item in serializer.validated_data])
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# Update customer
@api_view(['PUT'])
def updateCustomer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
        serializer = CustomerSerializer(instance=customer, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)

# Delete customer
@api_view(['DELETE'])
def deleteCustomer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
        customer.delete()
        return Response('Customer successfully deleted!', status=204)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)


# Get all tickets
@api_view(['GET'])
def getTickets(request):
    tickets = Ticket.objects.all()
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)

# Get a single ticket
@api_view(['GET'])
def getTicket(request, pk):
    try:
        ticket = Ticket.objects.get(id=pk)
        serializer = TicketSerializer(ticket, many=False)
        return Response(serializer.data)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found"}, status=404)



# Add ticket
@api_view(['POST'])
def addTicket(request):
    serializer = TicketSerializer(data=request.data, many=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# Update ticket
@api_view(['PUT'])
def updateTicket(request, pk):
    try:
        ticket = Ticket.objects.get(id=pk)
        serializer = TicketSerializer(instance=ticket, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found"}, status=404)

# Delete ticket
@api_view(['DELETE'])
def deleteTicket(request, pk):
    try:
        ticket = Ticket.objects.get(id=pk)
        ticket.delete()
        return Response('Ticket successfully deleted!', status=204)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found"}, status=404)


# Get all sellers
@api_view(['GET'])
def getSellers(request):
    sellers = Seller.objects.all()
    serializer = SellerSerializer(sellers, many=True)
    return Response(serializer.data)

# Get a single seller
@api_view(['GET'])
def getSeller(request, pk):
    try:
        seller = Seller.objects.get(id=pk)
        serializer = SellerSerializer(seller, many=False)
        return Response(serializer.data)
    except Seller.DoesNotExist:
        return Response({"error": "Seller not found"}, status=404)

# Add seller
@api_view(['POST'])
def addSeller(request):
    serializer = SellerSerializer(data=request.data, many=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# Update seller
@api_view(['PUT'])
def updateSeller(request, pk):
    try:
        seller = Seller.objects.get(id=pk)
        serializer = SellerSerializer(instance=seller, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except Seller.DoesNotExist:
        return Response({"error": "Seller not found"}, status=404)

# Delete seller
@api_view(['DELETE'])
def deleteSeller(request, pk):
    try:
        seller = Seller.objects.get(id=pk)
        seller.delete()
        return Response('Seller successfully deleted!', status=204)
    except Seller.DoesNotExist:
        return Response({"error": "Seller not found"}, status=404)


# Get all orders
@api_view(['GET'])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# Get a single order
@api_view(['GET'])
def getOrder(request, pk):
    try:
        order = Order.objects.get(id=pk)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

# Add order
@api_view(['POST'])
def addOrder(request):
    serializer = OrderSerializer(data=request.data, many=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# Update order
@api_view(['PUT'])
def updateOrder(request, pk):
    try:
        order = Order.objects.get(id=pk)
        serializer = OrderSerializer(instance=order, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

# Delete order
@api_view(['DELETE'])
def deleteOrder(request, pk):
    try:
        order = Order.objects.get(id=pk)
        order.delete()
        return Response('Order successfully deleted!', status=204)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)


# Filter orders by date or seller
@api_view(['GET'])
def filterOrders(request, filter_value):
    try:
        # Try to convert filter_value to a date
        filter_date = datetime.strptime(filter_value, "%Y-%m-%d").date()
        orders = Order.objects.filter(order_date=filter_date)
    except ValueError:
        # If it's not a date, try to find a seller by name
        try:
            seller = Seller.objects.get(name=filter_value)
            orders = Order.objects.filter(seller=seller)
        except Seller.DoesNotExist:
            return Response({"error": "Seller not found"}, status=404)

    # Serialize data and return
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
