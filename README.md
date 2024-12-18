# Video Frame Analysis and Hit Detection

This project processes video files to extract frames, detect edges, identify objects (balls), and calculate the number of "hits" based on ball proximity to predefined edges.

## Features

- Extracts frames from video files.
- Identifies left and right edges using Canny edge detection and Hough Line Transform.
- Detects ball coordinates using contour analysis and thresholding.
- Calculates hits based on proximity of detected balls to edges.
- Evaluates performance using Mean Absolute Error (MAE) against ground truth data.

## Prerequisites

- Required libraries include:
  - `numpy`
  - `opencv-python`
  - `scikit-learn`

## File Structure

- **Videos/**: Directory containing input video files.
- **Save/**: Directory where extracted frames will be saved.
- **res.txt**: File containing ground truth hit values for validation.

## Usage

### 1. Extract Frames
The script processes each video in the `Videos` directory and extracts frames to the `Save` directory using the `get_frames()` function.

### 2. Detect Edges
Edges of the playing area are identified using the `lr_edge` function. This step runs once for initialization and uses frame data to return left and right edge coordinates.

### 3. Detect Ball Coordinates
For each frame, ball coordinates are extracted using the `get_ball_coordinates` function, which leverages contour analysis to identify objects.

### 4. Calculate Hits
Hits are calculated using the `calculate_hits()` function, which compares ball coordinates to the left and right edge positions.

### 5. Evaluate Performance
The script compares detected hits against ground truth data from the `res.txt` file and calculates Mean Absolute Error (MAE) to measure accuracy.

## Functions Overview

### `get_res_from_txt(file)`
Reads ground truth hit values from a text file.

### `create_dir(path)`
Creates a directory if it does not exist.

### `save_frame(video_path, save_dir, gap)`
Extracts frames from a video and saves them to the specified directory.

### `lr_edge(frame)`
Detects left and right edges using Canny edge detection and Hough Line Transform.

### `get_ball_coordinates(frame)`
Detects ball coordinates in a frame based on contour analysis.

### `calculate_hits()`
Calculates the number of hits by comparing ball coordinates with edge positions.

## Sample Workflow

1. Call `get_frames()` to extract frames from videos.
2. Use `get_edges()` to initialize and retrieve edge coordinates.
3. Calculate hits for each video by calling `calculate_hits()`.
4. Load ground truth data using `get_res_from_txt('Videos/res.txt')`.
5. Compute the Mean Absolute Error (MAE) to evaluate the results.

## Sample Output
- Extracted frames are saved in the `Save/` directory.
- Example output for hits per video:
