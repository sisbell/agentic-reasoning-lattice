# Media Types

Source: Literary Machines, 3/4-3/5, 4/6-4/8 (pages 146-148, 175-176)

## What It Means

Xanadu is explicitly designed for ALL digital media, not just text. Nelson repeatedly emphasizes that the system handles "text, pictures, musical notations, photographs, recordings" and "any type of information" including graphics, 3D data, sound, DNA sequences, movies, symphonic scores, and CADCAM data.

The key architectural insight is that the byte-based addressing model is **media-agnostic**. Content is stored as bytes; interpretation is a front-end responsibility. The same span mechanism that addresses "this paragraph" in text can address "these pixels" in an image or "these samples" in audio - the system sees only bytes.

## User Guarantee

- **Any digital content** can be stored: text, images, audio, video, 3D models, scientific data
- **Same addressing** works for all media types - spans address bytes, not semantic units
- **Same linking** works across media - link from text to a region of an image
- **Same transclusion** works - include a portion of a video in your document
- **Same permanence** - all media types enjoy the same persistence guarantees

## Principle Served

**Format-agnostic storage for universal interconnection.** By working at the byte level rather than the semantic level, Xanadu avoids being locked to any particular media type or format. New media formats can be added without changing the addressing, linking, or storage architecture.

This serves the larger vision of the "docuverse" as a unified space for ALL human expression - not just writing, but all digital forms of literature, art, and data.

## What Requires Front-End Intelligence

The system stores and addresses bytes uniformly. Making sense of those bytes requires front-end knowledge:

- **Recognizing format** - Knowing bytes are JPEG vs WAV vs MPEG
- **Rendering content** - Displaying pixels, playing samples
- **Interpreting spans** - Translating "bytes 1000-2000" into "upper-left quadrant"
- **Enabling selection** - Letting users click on a video frame and create a span address

This is by design: Nelson explicitly says "Viewing-methods and manipulations are up to the designers of the equipment and viewing program" (2/47).

## Nelson's Words

> "All forms of material--text, pictures, musical notations, even photographs and recordings--may be digitally stored on it. Most importantly, the new forms of interconnection this makes possible among these materials are profound and revealing."
> (3/4)

> "The Xanadu document may have any structure (sequential or not) and may hold any type of information."
> (4/6)

> "At the user level, a Xanadu document may have any shape or form. It may consist of linear text or hypertext, possible graphics, 3D graphics or CADCAM data, scienter graphic data branches, movies, symphonic scores, and so on."
> (4/8)

> "Bit-map graphics will be stored in such a way as to allow panning (graphical scrolling) and zoom (continuously increasing or decreasing magnification) as incremental data deliveries."
> (3/4)

> "Three-dimensional objects, when implemented, may be collaged by users into compound objects, scenes from history, enactments, and artwork."
> (3/4)
