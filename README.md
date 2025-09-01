# CadQuery Test Script

## Running the Test Script

To run the CadQuery test script using Docker, use the following command:

```bash
docker run -v "$(pwd)":/workspace -w /workspace cadquery/cadquery python test_cadquery.py
```

## Command Breakdown

- `docker run` - Run a Docker container
- `--rm` - Automatically remove the container when it exits (prevents accumulating unused stopped containers that take up disk space)
  - To see all containers including stopped ones: `docker ps -a`
- `-v "$(pwd)":/workspace` - Mount the current directory to `/workspace` inside the container
- `-w /workspace` - Set the working directory inside the container to `/workspace`
- `cadquery/cadquery` - Use the CadQuery Docker image
- `python test_cadquery.py` - Execute the Python script

## What the Script Does

The test script creates a simple 3D part:
1. Creates a 20mm x 40mm rectangular sketch in the XY plane
2. Extrudes the sketch 10mm upward
3. Creates a 5mm diameter circular hole on the top face
4. Cuts the hole through the entire part (5mm deep pocket)
5. Exports the result as a STEP file to `output/test_part.step`

## Output

After running the command, you should see:
- A success message in the terminal
- A new STEP file at `output/test_part.step`
