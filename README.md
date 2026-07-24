# image_parsing_ocr
A POC to upload an image, parse it using PaddleOCR and identify important information using regexes and LLM

# Steps to run
1. Clone the repository
```
https://github.com/KarthikSJ97/image_parsing_ocr.git
```
2. Run the below command to get the service up and running. The first run might take some time as it needs to pull in the required packages
```
docker compose up --build   
```
3. Hit the /extract API. Below is the API collection for reference. Currently we support the following document types (aadhaar, pan, driving_license, passport)
[Download Bruno Collection Zip](https://github.com/KarthikSJ97/image_parsing_ocr/blob/main/image_parsing_ocr_api_collection.zip)
4. Run the below command to stop the server and close the docker container
```
docker compose down
```

# Note
This is specifically designed to work better for Indian ID card only
