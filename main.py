from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
import subprocess
import tempfile
import os
from enum import Enum
from pydantic import BaseModel
import cairosvg
from io import BytesIO

class OutputFormat(str, Enum):
    SVG = "svg"
    PNG = "png"

class NomnomlRequest(BaseModel):
    diagram: str
    format: OutputFormat = OutputFormat.SVG

app = FastAPI(title="Nomnoml Renderer")

@app.post("/render", response_class=Response)
async def render(request: NomnomlRequest):
    """
    Render nomnoml markup to SVG or PNG
    """
    try:
        # Create temporary files for the rendering process
        with tempfile.NamedTemporaryFile(suffix='.nomnoml', delete=False, mode='w') as nomnoml_file:
            nomnoml_file.write(request.diagram)
            nomnoml_path = nomnoml_file.name

        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as svg_file:
            svg_path = svg_file.name

        # Run nomnoml CLI tool to generate SVG
        process = subprocess.run(
            ['nomnoml', nomnoml_path, svg_path],
            capture_output=True,
            text=True,
            check=True  # This will raise CalledProcessError if the command fails
        )

        # Read the SVG data
        with open(svg_path, 'rb') as f:
            svg_data = f.read()

        # If PNG was requested, render the SVG to PNG
        if request.format == OutputFormat.PNG:
            # Convert SVG to PNG using cairosvg
            png_data = cairosvg.svg2png(bytestring=svg_data)
            response_data = png_data
            media_type = "image/png"
        else:
            response_data = svg_data
            media_type = "image/svg+xml"

        # Clean up temporary files
        os.unlink(nomnoml_path)
        os.unlink(svg_path)

        return Response(
            content=response_data,
            media_type=media_type
        )

    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Nomnoml rendering failed: {e.stderr}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during rendering: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    print("Starting server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)