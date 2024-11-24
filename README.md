# Nomnoml Renderer API

A FastAPI service that renders [Nomnoml](https://nomnoml.com) diagram markup to SVG or PNG formats. This service provides a REST API endpoint that accepts Nomnoml diagram syntax and returns the rendered diagram in your chosen format.

## Prerequisites

- Python 3.8+
- Node.js (for nomnoml CLI)
- Cairo graphics library (for PNG rendering)

## Installation

1. Install the nomnoml CLI tool:
```bash
npm install -g nomnoml
```

2. Install system dependencies (for Cairo):

On Ubuntu/Debian:
```bash
sudo apt-get install libcairo2-dev pkg-config
```

On macOS:
```bash
brew install cairo pkg-config
```

3. Clone the repository and install Python dependencies:
```bash
git clone <repository-url>
cd nomnoml-renderer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Server

Start the server with:
```bash
python main.py
```

The server will start on http://localhost:8000

## API Usage

### Render Endpoint

**POST** `/render`

Request body:
```json
{
    "diagram": "Your nomnoml diagram markup here",
    "format": "svg"  // or "png"
}
```

Example using curl:
```bash
curl -X POST http://localhost:8000/render \
  -H "Content-Type: application/json" \
  -d '{
    "diagram": "[Diagram]->[Rendered]",
    "format": "svg"
  }' \
  --output diagram.svg
```
### Example Diagram

Here's a simple example of a Nomnoml diagram you can try:

```nomnoml
[Nomnoml|
  [Renderer|
    +render(diagram: string): Image
  ]
]
```

Which will look like this:

![nomnoml.png](..%2F..%2FDownloads%2Fnomnoml.png)

## Documentation

API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Error Handling

The service returns appropriate HTTP status codes:
- 200: Successful rendering
- 400: Invalid request body
- 500: Rendering error or server error

Error responses include a detail message explaining what went wrong.

## Development

### Running Tests
```bash
pytest
```

### Code Style
This project follows PEP 8 guidelines. Format your code using:
```bash
black .
```

## License

[MIT License](LICENSE)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

If you encounter any problems, please file an issue along with a detailed description.