---
sidebar_position: 1
---
# `datatypes` module
The `datatypes` module provides three different classes which act as wrappers for different data types.

## `Image` data type
#### EXAMPLE:
```py
from textbase.datatypes import Image

# bot logic

    return {
            "messages": [Image(url=bot_response)],
            "state": state
        }
```
#### PARAMETERS:
- **url** - A publicly hosted URL for an image file.
- **pil_image** - A PIL image object.
- **path** - A path to an image file on your computer.

**NOTE**: All the above parameters are *mutually exclusive*.

#### RETURNS:
- A custom URL if a `pil_image` or a `path` is provided.
- The URL itself if `url` is provided.

#### RAISES:
- **TypeError** - If two or more parameters are provided simultaneously or if the PIL image is not valid.
- **FileNotFoundError** - If the image file path is invalid.

## `Video` data type
#### EXAMPLE:
```py
from textbase.datatypes import Video

# bot logic

    return {
            "messages": [Video(path="path/to/video/file.mp4")],
            "state": state
        }
```
#### PARAMETERS:
- **url** - A publicly hosted URL for a video file.
- **path** - A path to a video file on your computer.

**NOTE**: All the above parameters are *mutually exclusive*.

#### RETURNS:
- A custom URL if a `path` is provided.
- The URL itself if `url` is provided.

#### RAISES:
- **FileNotFoundError** - If the video file path is invalid.

## `Audio` data type
#### EXAMPLE:
```py
from textbase.datatypes import Audio

# bot logic

    return {
            "messages": [Audio(path="path/to/audio/file.mp3")],
            "state": state
        }
```
#### PARAMETERS:
- **url** - A publicly hosted URL for an audio file.
- **path** - A path to an audio file on your computer.

**NOTE**: All the above parameters are *mutually exclusive*.

#### RETURNS:
- A custom URL if a `path` is provided.
- The URL itself if `url` is provided.

#### RAISES:
- **FileNotFoundError** - If the audio file path is invalid.
