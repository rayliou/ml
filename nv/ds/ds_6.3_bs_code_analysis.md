
## Complete Lifecycle Analysis of `multi_src_tee_`

### **1. Initialization and Creation**

**File: `apps/buspas/PipelineCtrl.cpp`**
```100:109:apps/buspas/PipelineCtrl.cpp
void PipelineCtrl::attachTeeAfterMultiSrcs(
    GstElement *sourceElement, GstElement *originalSuccessiveElement,
    const char *teeName)
{
    multi_src_bin_ = sourceElement;
    multi_src_tee_ = gst_element_factory_make("tee", "multi_src_tee");
    if (!multi_src_tee_) {
        throw std::runtime_error("Failed to create element 'tee'");
    }
    gst_bin_add(GST_BIN(pipeline_), multi_src_tee_);
```

**Initialization Process:**
1. **Creation**: The tee is created using `gst_element_factory_make("tee", "multi_src_tee")`
2. **Pipeline Addition**: Added to the main pipeline using `gst_bin_add(GST_BIN(pipeline_), multi_src_tee_)`
3. **Reference Storage**: The tee reference is stored in `multi_src_tee_` member variable

### **2. Integration Point in Main Pipeline**

**File: `apps/sample_apps/deepstream-app/deepstream_app.c`**
```1527:1529:apps/sample_apps/deepstream-app/deepstream_app.c
buspas_attach_tee_after_multi_srcs(pipeline->pipeline
        ,pipeline->multi_src_bin.bin,last_elem);
```

**Integration Context:**
- **Timing**: Called during pipeline creation, after all main processing elements are set up
- **Position**: Inserted between `multi_src_bin` (source processing) and `last_elem` (sink processing)
- **Purpose**: Creates a branching point for additional processing streams (image capture, HLS)

### **3. Connection to Main Pipeline**

**File: `apps/buspas/PipelineCtrl.cpp`**
```110:125:apps/buspas/PipelineCtrl.cpp
NVGSTDS_LINK_ELEMENT(multi_src_bin_, multi_src_tee_);
GstPad *tee_src_pad, *last_elem_sink_pad;
tee_src_pad = gst_element_get_request_pad(multi_src_tee_, "src_%u");
if (!tee_src_pad) {
    throw std::runtime_error("Failed to get request pad from 'tee'");
}
last_elem_sink_pad =
    gst_element_get_static_pad(originalSuccessiveElement, "sink");
if (!last_elem_sink_pad) {
    throw std::runtime_error("Failed to get static pad from 'last_elem'");
}

if (gst_pad_link(tee_src_pad, last_elem_sink_pad) != GST_PAD_LINK_OK) {
    throw std::runtime_error("Failed to link tee and last_elem");
}
```

**Connection Architecture:**
```
[multi_src_bin] → [multi_src_tee_] → [original_successive_element]
                       ↓
                  [dynamic branches]
                  (ImageCaptureBin, HLS, etc.)
```

**Connection Details:**
1. **Input Connection**: `multi_src_bin_` → `multi_src_tee_` (using `NVGSTDS_LINK_ELEMENT`)
2. **Main Output**: `multi_src_tee_` → `originalSuccessiveElement` (using request pad)
3. **Dynamic Outputs**: Additional request pads for sink bins

### **4. Dynamic Branch Management**

**File: `apps/buspas/BaseSinkBin.cpp`**
```150:175:apps/buspas/BaseSinkBin.cpp
void BaseSinkBin::enableAfterTee(GstElement *tee)
{
    if (!created_) {
        create();
        created_ = true;
    }
    tee_ = tee;

    GstPad *teeSrcPad = gst_element_get_request_pad(tee_, "src_%u");
    GstPad *curBinSinkPad = gst_element_get_static_pad(selfBin_, "sink");
    if (!teeSrcPad) {
        std::cerr << __FUNCTION__ << ": Failed to get tee src pad" << std::endl;
        throw std::runtime_error(__FUNCTION__ +
                                 std::string(": Failed to get tee src pad"));
    }
    if (!curBinSinkPad) {
        std::cerr << __FUNCTION__ << ": Failed to get bin sink pad"
                  << std::endl;
        throw std::runtime_error(__FUNCTION__ +
                                 std::string(": Failed to get bin sink pad"));
    }
    debugPrintRefCount(selfBin_, "BaseSinkBin", __FUNCTION__, __LINE__);

    if (gst_pad_link(teeSrcPad, curBinSinkPad) != GST_PAD_LINK_OK) {
        std::cerr << "Failed to link tee to bin " << name_
                  << " (tee src pad: " << GST_PAD_NAME(teeSrcPad)
                  << ", bin sink pad: " << GST_PAD_NAME(curBinSinkPad) << ")"
                  << std::endl;
    }
    else {
        std::cout << "Bin " << name_ << " linked successfully." << std::endl;
    }
```

**Dynamic Branch Process:**
1. **Request Pad**: Each sink bin requests a new source pad from tee using `gst_element_get_request_pad(tee_, "src_%u")`
2. **Linking**: The tee source pad is linked to the sink bin's ghost pad
3. **State Sync**: Sink bin state is synchronized with the pipeline
4. **Activation**: The branch becomes active and starts receiving data

### **5. Branch Disconnection and Cleanup**

**File: `apps/buspas/BaseSinkBin.cpp`**
```200:225:apps/buspas/BaseSinkBin.cpp
void BaseSinkBin::disable()
{
    if (!running_) {
        return;
    }
    if (!tee_ || !selfBin_) {
        std::cerr << "Tee or SinkBin is not initialized" << std::endl;
        return;
    }
    GstPad *sinkBinSinkPad = gst_element_get_static_pad(selfBin_, "sink");
    GstPad *teeSrcPad = gst_pad_get_peer(sinkBinSinkPad);

    if (teeSrcPad) {
        if (!gst_pad_unlink(teeSrcPad, sinkBinSinkPad)) {
            std::cerr << "Failed to unlink tee from sink bin" << std::endl;
        }
        else {
            std::cout << "Tee unlinked from sink bin successfully."
                      << std::endl;
        }
        // Release the request pad from the tee
        gst_element_release_request_pad(tee_, teeSrcPad);
        std::cout << "Request pad released from tee." << std::endl;
    }
```

**Cleanup Process:**
1. **Unlinking**: Disconnect the tee source pad from sink bin
2. **Pad Release**: Release the request pad back to the tee using `gst_element_release_request_pad()`
3. **State Change**: Set sink bin to NULL state
4. **Resource Cleanup**: Free all associated resources

### **6. Tee Usage Patterns**

**Image Capture Usage:**
```178:178:apps/buspas/PipelineCtrl.cpp
imageCaptureBin_->enableAfterTee(multi_src_tee_);
```

**HLS Streaming Usage:**
```192:192:apps/buspas/PipelineCtrl.cpp
httpLiveStreamingBin_->enableAfterTee(multi_src_tee_);
```

### **7. Pipeline State Management**

**File: `apps/buspas/PipelineCtrl.cpp`**
```65:75:apps/buspas/PipelineCtrl.cpp
void PipelineCtrl::onFirstPlayingState()
{
    logger.info("First playing state");
    auto &after_camera = Configure::instance().after_camera_;
    logger.info("Starting HLS or image capture according to the configuration below:");
    after_camera.print();
    if (after_camera.enable_capture_image_on_start) {
        captureImageAfterMultiSrcs(nullptr, nullptr, nullptr);
    }
    if (after_camera.enable_hls) {
        if (after_camera.enable_capture_image_on_start) {
            g_timeout_add(50, aSyncStartHttpLiveStreamingAfterMultiSrcs, this);
```

**State Management:**
- **Pipeline Playing**: Tee becomes active when pipeline reaches PLAYING state
- **Auto-start Features**: Automatic image capture and HLS streaming based on configuration
- **Dynamic Control**: Branches can be added/removed during runtime

### **8. Memory and Resource Management**

**Tee Lifecycle:**
1. **Creation**: During pipeline setup via `buspas_attach_tee_after_multi_srcs()`
2. **Active Phase**: Distributes data to multiple branches
3. **Cleanup**: Automatic cleanup when pipeline is destroyed (GStreamer handles this)

**Key Points:**
- **No Explicit Cleanup**: The tee itself is not explicitly destroyed in `PipelineCtrl::destroy()`
- **GStreamer Management**: GStreamer automatically cleans up the tee when the pipeline is destroyed
- **Request Pad Management**: Individual sink bins are responsible for releasing their request pads

### **9. Error Handling and Robustness**

**Error Scenarios:**
- **Creation Failure**: Throws runtime exception if tee creation fails
- **Linking Failure**: Throws runtime exception if linking fails
- **Pad Request Failure**: Throws runtime exception if request pad cannot be obtained

**Robustness Features:**
- **State Checking**: Verifies pipeline state before operations
- **Resource Validation**: Checks for null pointers before operations
- **Graceful Degradation**: Individual branch failures don't affect main pipeline

### **Summary**

The `multi_src_tee_` serves as a critical branching point in the DeepStream pipeline, enabling:

1. **Main Data Flow**: Continues the primary processing pipeline
2. **Dynamic Branches**: Supports runtime addition of image capture and HLS streaming
3. **Resource Efficiency**: Shares the same video stream across multiple outputs
4. **Flexible Architecture**: Allows independent control of each branch

The tee's lifecycle is tightly integrated with the main pipeline, created once during initialization and managed automatically by GStreamer's reference counting system. Individual branches manage their own connection/disconnection lifecycle while the tee remains persistent throughout the application's lifetime.


## Image Capture Code Analysis

The image capture functionality in this DeepStream application is implemented through a command-based system using named pipes. Here's a detailed breakdown of all the related code and how it works:

### 1. **Command Reception System**

**File: `apps/buspas/CommandNamedPipe.cpp`**
- **Named Pipe Setup**: The system creates a named pipe (FIFO) for receiving external commands
- **Command Processing Thread**: `buspas_event_thread_func()` runs periodically (every 100ms) to check for new commands
- **Command Parsing**: Commands are parsed from the pipe and executed via `executeCommand()`

```47:50:apps/buspas/CommandNamedPipe.cpp
<< "- capture_image [image_path]\n"
<< "   - Capture an image from the pipeline.\n"
<< "   - Usage: capture_image (uses default path)\n"
<< "   - Usage: capture_image /path/to/image.jpg\n\n"
```

### 2. **Image Capture Command Handler**

**File: `apps/buspas/CommandNamedPipe.cpp`**
```184:185:apps/buspas/CommandNamedPipe.cpp
if (command == "capture_image") {
    buspas_async_capture_image_after_multi_srcs(argument.empty() ? nullptr : argument.c_str(), onSuccessCaptureImage, onFailureCaptureImage);
```

The `capture_image` command:
- Accepts an optional image path parameter
- Uses default path if no parameter provided
- Calls the async capture function with success/failure callbacks

### 3. **Image Capture Orchestration**

**File: `apps/buspas/PipelineCtrl.cpp`**
```143:178:apps/buspas/PipelineCtrl.cpp
void PipelineCtrl::captureImageAfterMultiSrcs(const char *image_path, 
                                            buspas_capture_callback onSuccess,
                                            buspas_capture_callback onFailure)
{
    // The previous image capture bin will be disabled automatically when
    // destructed
    if (imageCaptureBin_) {
        logger.error("Image capture bin is running, disable or wait for it to finish");
        if (onFailure) {
            onFailure(imageFilePath_.c_str());
        }
        return;
    }
    auto &configure = Configure::instance();
    auto &after_camera = configure.after_camera_;
    if (image_path) {
        imageFilePath_ = image_path;
    }
    else {
        imageFilePath_ = after_camera.capture_image_dir + "/" +
                         configure.hostName_ + ".jpg";
    }
    imageCaptureBin_ = new ImageCaptureBin(pipeline_, imageFilePath_);
    imageCaptureBin_->onFileWritten([this, onSuccess]() {
        imgCaptureOnStartDone_  = true;
        if (onSuccess) {
            onSuccess(imageFilePath_.c_str());
        }
        delete imageCaptureBin_;
        imageCaptureBin_ = nullptr;
        logger.warn("Image capture bin deleted, image file path: %s", imageFilePath_.c_str());
        imageFilePath_.clear();
        return;
    });
    logger.info("Enabling image capture bin, image file path: %s", imageFilePath_.c_str());
    imageCaptureBin_->enableAfterTee(multi_src_tee_);
}
```

This function:
- Prevents multiple simultaneous captures
- Generates default filename using hostname if no path specified
- Creates an `ImageCaptureBin` instance
- Sets up completion callback for cleanup
- Enables the capture bin after the tee element

### 4. **Image Capture Implementation**

**File: `apps/buspas/ImageCaptureBin.cpp`**
```41:64:apps/buspas/ImageCaptureBin.cpp
void ImageCaptureBin::create()
{
    auto *selfBin = getSelfBin();
    debugPrintRefCount(selfBin, "selfBin", __FUNCTION__, __LINE__);

    auto *queue = gst_element_factory_make("queue", NULL);
    auto *nvvidconv = gst_element_factory_make("nvvidconv", NULL);
    auto *nvjpegenc = gst_element_factory_make("nvjpegenc", NULL);
    multifilesink_ = gst_element_factory_make("multifilesink", NULL);

    g_object_set(multifilesink_, "location", location_.c_str(), "post-messages", TRUE, NULL);

    gst_bin_add_many(GST_BIN(selfBin), queue, nvvidconv, nvjpegenc,
                     multifilesink_, NULL);
    debugPrintRefCount(selfBin, "selfBin", __FUNCTION__, __LINE__);

    if (!gst_element_link_many(queue, nvvidconv, nvjpegenc, multifilesink_,
                              NULL)) {
        logger.error("Failed to link elements in the image capture bin");
    }
    debugPrintRefCount(selfBin, "selfBin", __FUNCTION__, __LINE__);
    setupGhostPad(queue);
}
```

The GStreamer pipeline for image capture:
- **queue**: Buffers video frames
- **nvvidconv**: NVIDIA video converter for format conversion
- **nvjpegenc**: NVIDIA JPEG encoder for compression
- **multifilesink**: Saves the encoded image to file

### 5. **Capture Detection and Cleanup**

**File: `apps/buspas/ImageCaptureBin.cpp`**
```81:103:apps/buspas/ImageCaptureBin.cpp
GstPadProbeReturn ImageCaptureBin::padProbeCallback(GstPad *pad,
                                                    GstPadProbeInfo *info,
                                                    gpointer userData)
{
    ImageCaptureBin *self = static_cast<ImageCaptureBin *>(userData);

    if (self->isRunning() &&
        GST_PAD_PROBE_INFO_TYPE(info) & GST_PAD_PROBE_TYPE_BUFFER) {
        if (self->isFirstFileWriten()) {
            self->disable();
            self->postCapture(self->location_);
            return GST_PAD_PROBE_REMOVE;
        }
        else {
            logger.info("First file is not written, continue capture");
            return GST_PAD_PROBE_OK;
        }

    }
    logger.info("Image capture bin is still running");
    return GST_PAD_PROBE_OK;
}
```

The pad probe:
- Monitors buffer flow through the pipeline
- Checks if the image file has been written to disk
- Automatically disables the capture bin after successful capture
- Triggers the completion callback

### 6. **Configuration System**

**File: `apps/buspas/Configure.h`**
```14:17:apps/buspas/Configure.h
struct ConfSectionAfterCamera
{
    bool enable_capture_image_on_start;
    std::string capture_image_dir;
    // ... other fields
```

**File: `conf/current.txt`**
```203:210:conf/current.txt
[buspas]
command-pipe-file=./default_command_pipe

[after-camera]
enable-capture-image-on-start=1
capture-image-dir=/var/buspas_ds_detection/data/imagecaptured/
```

Configuration settings:
- **command-pipe-file**: Path to the named pipe for commands
- **capture-image-dir**: Default directory for saved images
- **enable-capture-image-on-start**: Auto-capture on pipeline start

### 7. **Integration with Main Application**

**File: `apps/deepstream_app_main.c`**
```793:795:apps/deepstream_app_main.c
g_timeout_add (200, buspas_event_on_first_playing_state, appCtx[0]);
g_timeout_add (100, buspas_event_thread_func, appCtx[0]);
g_timeout_add (40, event_thread_func, NULL);
```

The main application:
- Sets up periodic timers for command processing
- Integrates the command system with the GStreamer main loop
- Handles pipeline state changes

### **Complete Flow Summary**

1. **Initialization**: Named pipe is created at application startup
2. **Command Reception**: External process writes "capture_image [path]" to the pipe
3. **Command Processing**: Timer-based thread reads and parses the command
4. **Pipeline Setup**: Creates a new ImageCaptureBin with GStreamer elements
5. **Tee Connection**: Connects the capture bin to the main pipeline via tee element
6. **Image Capture**: Video frames flow through the capture pipeline and get saved as JPEG
7. **Completion Detection**: Pad probe detects when file is written
8. **Cleanup**: Capture bin is disabled and deleted, callbacks are triggered

This system allows external applications to trigger image capture by simply writing commands to the named pipe, making it very flexible for integration with other systems.

