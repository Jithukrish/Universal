# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
# from .models import ProductPage

# from .serializers import ProductPageSerializer, ProductPageDetailSerializer
# from django.core.paginator import Paginator


# class ProductCategoryViewSet(viewsets.ModelViewSet):
#     serializer_class = ProductPageSerializer

#     def get_serializer_class(self):
#         group_serializer = {
#             'list': ProductPageSerializer,
#             'retrieve': ProductPageDetailSerializer,
#         }
#         return group_serializer.get(self.action, self.serializer_class)

    


#     def get_queryset(self):
#         queryset = ProductPage.objects.live()
        

#         # name filter ----------------------------------------- 
#         name_filter = self.request.query_params.get('name')
#         if name_filter:
#             queryset = queryset.filter(title__icontains=name_filter)

#         tag_filter = self.request.query_params.get('tag') 
#         print("tag_filter--------------", tag_filter)  
#         if tag_filter:
#             print("inside tag filter--------------", tag_filter)

#             tag_filter_list = [tag.strip() for tag in tag_filter.split(',')]

#             filtered_products = []
#             for product in queryset:
#                 for block in product.content:
#                     if block.block_type == 'product_details':
#                         tags = block.value['tags'] 
#                         if any(tag in tags for tag in tag_filter_list):  
#                             filtered_products.append(product)
#                             break  

#             queryset = queryset.filter(id__in=[product.id for product in filtered_products])

#         category_slug = self.request.query_params.get('category')
#         if category_slug:
#             category_slug = category_slug.rstrip('/') 
#             try:
#                 category = ProductCategory.objects.get(slug__iexact=category_slug)
#                 queryset = queryset.child_of(category)
#             except ProductCategory.DoesNotExist:
#                 return ProductPage.objects.none()

        
#         return queryset


      

#     def list(self, request, *args, **kwargs):
#         response = {}
#         try:
#             limit = int(request.GET.get('limit', PAGINATION_PER_PAGE))
#             page = int(request.GET.get('page', 1))
#             queryset = self.get_queryset()
#             if not queryset.exists():
#                 return Response({"result": "failure", "message": "No products found."}, status=status.HTTP_404_NOT_FOUND)

#             paginator = Paginator(queryset, limit)
#             records = paginator.get_page(page)
#             serializer = self.get_serializer(records, many=True, context={'request': request})
#             response['result'] = 'success'
#             response['records'] = serializer.data
#             response['page_count'] = paginator.count
#             response['has_next'] = records.has_next()
#             response['has_previous'] = records.has_previous()
#             response['pages'] = paginator.num_pages
#         except Exception as e:
#             response['result'] = 'failure'
#             response['message'] = str(e)
#             return Response(response, status=status.HTTP_400_BAD_REQUEST)
#         return Response(response, status=status.HTTP_200_OK)

   
   
  
#     def retrieve(self, request, slug=None):
#         print("Retrieve method called")
#         response = {}
#         try:
#             product_page = get_object_or_404(ProductPage, slug=slug)
#             print("Product page retrieved successfully:", product_page)
            
#             serializer = self.get_serializer(product_page, context={'request': request})
#             response['result'] = 'success'
#             response['records'] = serializer.data
#             response['product_id'] = product_page.id
#             print(f"Product ID: {response['product_id']}")
            
#         except Page.DoesNotExist:
#             return Response({"result": "failure", "message": "No ProductPage matches the given query."}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             response['result'] = 'failure'
#             response['message'] = str(e)

#         return Response(response, status=status.HTTP_200_OK)


 


        