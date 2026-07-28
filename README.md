# image_parsing_ocr

A document extraction service that accepts document images, processes them using PaddleOCR, and extracts important information using document-specific parsers and field extractors.

The service is designed to identify and extract structured information from documents such as:

- Aadhaar Card
- PAN Card
- Driving License
- Passport
- Flight Tickets (TBA)
- IRCTC Tickets (TBA)

The goal is to demonstrate an extensible OCR pipeline where OCR processing, document identification, and field extraction are separated into independent layers.

---

# Architecture Overview

The extraction pipeline follows a layered architecture:

```
                Client
                  |
                  |
             FastAPI API
                  |
                  |
        Extraction Service Layer
                  |
                  |
          Image Preprocessing
                  |
                  |
           PaddleOCR Adapter
                  |
                  |
             OCR Models
                  |
                  |
        Document Navigation Layer
                  |
                  |
          Document Parser Layer
                  |
                  |
          Field Extractors
                  |
                  |
          Structured JSON Response
```

## Processing Flow

1. Client uploads a document image.
2. API validates the request and stores the uploaded file temporarily.
3. Image preprocessing optimizes the input image:
   - Resize large images
   - Reduce memory consumption
   - Maintain aspect ratio
4. PaddleOCR extracts text, coordinates, and confidence information.
5. OCR output is converted into internal document models.
6. Document navigation identifies the appropriate parser.
7. Parser invokes document-specific field extractors.
8. Extracted fields are returned as structured JSON.

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python 3.11 |
| API Framework | FastAPI |
| OCR Engine | PaddleOCR |
| Image Processing | Pillow |
| Containerization | Docker |
| Container Orchestration | Docker Compose |
| API Testing | Bruno |
| Extraction Logic | Regex-based extractors + document-specific parsers |
| Configuration | Python based configuration modules |
| Architecture Pattern | Adapter + Registry + Strategy patterns |

---

# Project Structure

```
image_parsing_ocr/
│
├── ocr-service/
│   │
│   ├── api/
│   │   ├── routes.py                  # REST API endpoints
│   │   └── __init__.py
│   │
│   ├── core/
│   │   ├── paddle_adapter.py          # PaddleOCR integration layer
│   │   └── __init__.py
│   │
│   ├── navigation/
│   │   ├── document_navigator.py      # Routes documents to correct parser
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── extraction_service.py      # Main extraction workflow orchestration
│   │   └── __init__.py
│   │
│   ├── parsers/
│   │   ├── base_parser.py             # Common parser interface
│   │   ├── parser_registry.py         # Parser registration and lookup
│   │   ├── aadhaar_parser.py           # Aadhaar parser
│   │   ├── pan_parser.py               # PAN parser
│   │   ├── passport_parser.py           # Passport parser
│   │   ├── driving_license_parser.py    # Driving license parser
│   │   ├── flight_parser.py             # Flight ticket parser
│   │   └── irctc_parser.py              # IRCTC parser
│   │
│   ├── extractors/
│   │   ├── base_extractor.py           # Common extractor interface
│   │   ├── regex_extractor.py           # Generic regex extraction
│   │   ├── aadhaar_*_extractor.py       # Aadhaar field extractors
│   │   ├── pan_*_extractor.py           # PAN field extractors
│   │   ├── passport_*_extractor.py      # Passport field extractors
│   │   └── driving_license_*_extractor.py
│   │                                    # Driving license field extractors
│   │
│   ├── configs/
│   │   ├── aadhaar.py                   # Aadhaar extraction configuration
│   │   ├── pan.py                       # PAN extraction configuration
│   │   ├── passport.py                  # Passport extraction configuration
│   │   └── driving_license.py           # Driving license configuration
│   │
│   ├── models/
│   │   ├── ocr_document.py              # OCR document representation
│   │   ├── ocr_page.py                  # OCR page representation
│   │   ├── ocr_line.py                  # OCR text line representation
│   │   ├── ocr_region.py                # OCR region/bounding box model
│   │   ├── ocr_field.py                 # Extracted field model
│   │   ├── extraction_result.py         # Extraction result model
│   │   ├── document_type.py             # Supported document types
│   │   └── point.py                     # Coordinate representation
│   │
│   ├── schemas/
│   │   └── aadhaar_schema.py            # API response schema definitions
│   │
│   ├── utils/
│   │   ├── text_utils.py                # Text processing utilities
│   │   ├── geometry_utils.py            # OCR coordinate utilities
│   │   └── __init__.py
│   │
│   ├── config.py                        # Application configuration
│   ├── app.py                           # FastAPI application entry point
│   ├── requirements.txt                 # Python dependencies
│   ├── Dockerfile                       # Docker image definition
│   └── .dockerignore
│
├── docker-compose.yml                   # Container orchestration
├── image_parsing_ocr_api_collection.zip # Bruno API collection
├── LICENSE
└── README.md
```

---

# Supported Documents

Currently supported document types:

| Document | Status |
|----------|--------|
| Aadhaar Card | Supported |
| PAN Card | Supported |
| Driving License | Supported |
| Passport | Supported |
| Flight Ticket | TBA |
| IRCTC Ticket | TBA |

The extraction logic is currently optimized primarily for Indian identity documents.

---

# Running the Application

## 1. Clone Repository

Clone the repository:

```bash
git clone https://github.com/KarthikSJ97/image_parsing_ocr.git
```

Navigate into the repository:

```bash
cd image_parsing_ocr
```

---

## 2. Start the Service

Run:

```bash
docker compose up --build
```

The first execution may take some time because Docker needs to:

- Build the application image
- Install Python dependencies
- Download PaddleOCR models

Once started, the API will be available locally.

---

## 3. Test the API

Use the provided Bruno collection:

[Download Bruno Collection Zip](https://github.com/KarthikSJ97/image_parsing_ocr/blob/main/image_parsing_ocr_api_collection.zip)

API endpoint:

```
POST /extract
```

Request:

```
multipart/form-data

document_type = aadhaar

file = aadhaar_image.png
```

Example response:

```json
{
  "document_type": "aadhaar",
  "name": "Karthik Jhingade",
  "aadhaar_number": "XXXX XXXX XXXX"
}
```

---

## 4. Stop the Service

To stop the running containers:

```bash
docker compose down
```

---

# OCR Enhancements

## Document Orientation Handling

The OCR pipeline supports:

```python
PaddleOCR(
    lang=settings.OCR_LANGUAGE,
    use_doc_orientation_classify=True,
    use_doc_unwarping=True,
    use_textline_orientation=True
)
```

This improves extraction accuracy for:

- Rotated documents
- Incorrectly oriented scans
- Perspective-distorted images

---

# Image Optimization and Memory Handling

High-resolution mobile images can consume significant memory during OCR processing.

To improve service stability, images are normalized before OCR inference.

The preprocessing flow includes:

- Resize large images
- Preserve aspect ratio
- Compress images before OCR processing

Example:

```
Original Image

6000 x 4000 pixels

        |
        |
Image Optimization

        |
        |

1200 x 800 pixels

        |
        |
PaddleOCR Processing
```

Benefits:

- Reduced memory consumption
- Faster OCR processing
- Reduced chance of container restart due to memory spikes

---

# Design Principles

## OCR Adapter

`core/paddle_adapter.py`

The adapter isolates PaddleOCR-specific implementation.

Benefits:

- OCR engine can be replaced in the future
- Business logic remains independent

Possible future integrations:

- Google Vision OCR
- AWS Textract
- Azure Document Intelligence

---

## Parser Registry

`parsers/parser_registry.py`

Instead of maintaining large conditional logic:

```
if document_type == "aadhaar":
    AadhaarParser()

elif document_type == "passport":
    PassportParser()
```

the registry dynamically maps:

```
Document Type
       |
       |
Parser Registry
       |
       |
Document Parser
```

Benefits:

- Easy addition of new document types
- Better maintainability
- Reduced code coupling

---

## Field Extractors

Extractors are responsible for individual field extraction.

Example:

```
Passport Parser

        |
        |
        +-- Passport Number Extractor
        |
        +-- Name Extractor
        |
        +-- DOB Extractor
        |
        +-- Nationality Extractor
```

This allows individual extraction rules to evolve independently.

---

# Limitations

- OCR accuracy depends on input image quality
- New document formats require additional parsers and extractors
- Handwritten text extraction is not supported
- Complex layouts may require advanced document understanding models
- Current extraction rules are optimized for known document formats

---

# Future Improvements

## LLM-based Document Understanding

Current:

```
OCR
 |
Regex / Extractors
 |
Structured JSON
```

Future:

```
OCR
 |
Vision Language Model
 |
Validation Layer
 |
Structured JSON
```

Benefits:

- Support unknown document formats
- Reduce parser maintenance
- Better handling of complex layouts

---

## Async Processing

For large-scale document processing:

```
Upload API

    |

Message Queue

    |

OCR Workers

    |

Extraction Service

    |

Database
```

Possible technologies:

- Kafka
- RabbitMQ
- AWS SQS

---

## Confidence Based Validation

Add confidence scoring:

```json
{
  "passport_number": {
      "value": "ZXXXXXX2",
      "confidence": 0.98
  }
}
```

Low-confidence fields can be routed for manual verification.

---

# Note

This is specifically designed and optimized for Indian identity documents and may require additional tuning for other document types.
