# Use Ubuntu as the base image
FROM ubuntu:latest

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install necessary packages
RUN apt-get update && apt-get install -y \
    git \
    sudo \
    openjdk-11-jdk \
    && apt-get clean

# Set JAVA_HOME and update PATH
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Clone the repository
RUN git clone https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp.git

# Create build directory
RUN mkdir -p amazon-kinesis-video-streams-producer-sdk-cpp/build

# Change working directory
WORKDIR /amazon-kinesis-video-streams-producer-sdk-cpp/build

# Install necessary dependencies
RUN apt-get --fix-broken install -y && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    cpp-13 \
    cpp-13-x86-64-linux-gnu \
    gcc \
    gcc-13 \
    gcc-x86-64-linux-gnu \
    gcc-13-x86-64-linux-gnu && \
    apt-get clean && \
    apt-get autoremove -y && \
    apt-get install -f -y && \
    apt-get install -y \
    libssl-dev \
    libcurl4-openssl-dev \
    liblog4cplus-dev \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    gstreamer1.0-plugins-base-apps \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-tools \
    build-essential \
    cmake \
    m4

# Run CMake to configure the project and build it
RUN cmake .. -DBUILD_GSTREAMER_PLUGIN=ON -DBUILD_JNI=TRUE && \
    make && \
    export GST_PLUGIN_PATH=`pwd`/build && \
    export LD_LIBRARY_PATH=`pwd`/open-source/local/lib

# Set environment variables
ENV GST_PLUGIN_PATH=/amazon-kinesis-video-streams-producer-sdk-cpp/build
ENV LD_LIBRARY_PATH=/amazon-kinesis-video-streams-producer-sdk-cpp/open-source/local/lib

# Copy entrypoint script into the container
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
