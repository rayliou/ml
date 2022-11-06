# Determine the target platform
PLATFORM ?= KNOWLES
PLATFORM ?= LINUX

SRC ?= afloat_real.cpp
# Compiler and flags for Linux
ifeq ($(PLATFORM), LINUX)
	INCS=-I./projects/TWS_small_Mnet_Nano/sdk_knowles/knowles/include
CXX = g++
CXXFLAGS = -std=c++11 -Wall
TARGET = SimuCore_Linux
endif

# Compiler and flags for Knowles
ifeq ($(PLATFORM), KNOWLES)
KNOWLES_REPO=/home/xiaorui/W/knowles_repos_fluent/w
CC_BIN = /data/micro/xtensa/tools/RI-2020.4-linux/XtensaTools/bin
#INCS=-I./projects/TWS_small_Mnet_Nano/sdk_knowles/knowles/include
INCS=-I/data/micro/Knowles_IA8201_SDK-7.0.1/Knowles_IA8201_SDK/Rome/Src/Cores/AVL/DMX1A
INCS+= -I/data/micro/Knowles_IA8201_SDK-7.0.1/Knowles_IA8201_SDK/Rome/Src/Cores/Core_Dmx1a/Include/
INCS+= -I/data/micro/Knowles_IA8201_SDK-7.0.1/Knowles_IA8201_SDK/Rome/Src/Cores/AVL/
#LIBS = -lfluentai-micro -lcmsis5_nn -lcmsis5_dsp  
LIBS +=-L./projects/TWS_small_Mnet_Nano/sdk_knowles/knowles/lib 
LIBS += $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/DSP/Libs/xccDSPLib.a \
    $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/Utility/Libs/xccUtilsBasicLib.a \
    $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/Utility/Libs/xccUtilsKnSRCLib.a \
    $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/Utility/Libs/xccUtilsRAFLib.a \
    $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/Utility/Libs/UtilsSupportLib.a \
    $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/Utility/Libs/DspFrameLib.a \
    $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/Utility/Libs/DspSampleLib.a \
    $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/MachineLearning/Libs/xccMachineLearningLib.a

# LIBS+= $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/DSP/Libs/xccDSPLib.a
# LIBS+= $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/Utility/Libs/xccUtilsBasicLib.a
# LIBS+= $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/Utility/Libs/xccUtilsKnSRCLib.a
# LIBS+= $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/Utility/Libs/xccUtilsRAFLib.a
# LIBS+= $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/Utility/Libs/UtilsSupportLib.a
# LIBS+= $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/Utility/Libs/DspFrameLib.a
# LIBS+= $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/Utility/Libs/DspSampleLib.a
# LIBS+= $(KNOWLES_REPO)/Rome/Src/Cores/Core_Dmx1a/MachineLearning/Libs/xccMachineLearningLib.a
CXX = $(CC_BIN)/xt-clang++
CXXFLAGS = -DAVL_DMX1A -g -Wall -g3 -O0 -Os -std=c++17 -fno-exceptions -ffunction-sections -fdata-sections -DDMX1A -DSIMULATION_BUILD
#CXXFLAGS += -Werror
TARGET = afloat_real
endif

all: $(TARGET)

$(TARGET): $(SRC) real_custom.hpp
	$(CXX) $(CXXFLAGS) -o $(TARGET)  $(SRC) $(LIBS) $(INCS)

clean:
	rm -f $(TARGET)

run: $(TARGET)
	/data/micro/xtensa/tools/RI-2020.4-linux/XtensaTools/bin/xt-run --turbo $<
gdb:$(TARGET)
	/data/micro/xtensa/tools/RI-2020.4-linux/XtensaTools/bin/xt-gdb --args $<
