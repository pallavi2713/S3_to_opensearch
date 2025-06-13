# S3_to_opensearch trigger
![image](https://github.com/user-attachments/assets/21eb5fea-8b4b-41ba-8aa0-37819eb3ccc5)

1. create open search domain
   
   domain creation method - standard create
   
   template  -dev/test

   deployment- domain without standby

   availablity xone -  1 AZ

   Enable compatility mode

   number of data node -  1

   instance - general purpose
 
   instance type-  t3.small.search

   network -- public access

   uncheck - enable fine grained access

   configure domain level access policy ->>> JSON
   
3. create policy using es-policy
   
    replace, region account_id , opensearch_domain name that you are creating

   replace ip ex -- 12.33.445.43/32 --add /32 at end

it will take 20 mis to create


Go to opensearch dashboard -> dev tools ->run book-index

![image](https://github.com/user-attachments/assets/3f0740f3-eb2e-4384-8621-9faca9f81c48)

![image](https://github.com/user-attachments/assets/55135fca-711d-4559-adde-e21825ed3de7)



4. create lambda function

5. set policy using lambda-policy

6. give a unique bucket name
7. then crete a bucket with same name
8. add trigger to lambda function -> add S3 choose your bucket

9. upload Zip in code editor

    ![image](https://github.com/user-attachments/assets/6b05c4dd-4a0d-4767-baf1-c4ce8412c762)

11. Add two environment variables to the lambda function.
      CONFIGURATION -> ENVIORNMENT VARIABLES
      ES_HOST - OpenSearch domain endpoint host ( without https//: and last / , no slashes required ) example :  search-project-domain-5veck3ynxydmkclxlkmkllje4irucbelcoita.eu-north-1.es.amazonaws.com
      ES_INDEX - OpenSearch index name  ( books in our case)
    ![image](https://github.com/user-attachments/assets/f2797d64-d705-4b95-8f9b-3dcc67650501)

12. cntrl + S ->> DEPLOY
13. upload sample.json to bucket
14. Go to monitor - >> cloud watch logs --> click topmost log
15. again run put request in opensearch
16. New records from sample file will be visible
    ![image](https://github.com/user-attachments/assets/6aeaa20d-0752-43df-bd36-129e1b72834c)

    ![image](https://github.com/user-attachments/assets/e41a3ef1-d0f6-4ed8-9956-3304469e159d)


   
   
   
   
