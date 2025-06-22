# ---- Build stage ----
FROM debian:stable AS builder
RUN apt update && apt install -y \
    build-essential \
    cmake \
    git \
    qt6-base-dev \
    libeigen3-dev \
    libturbojpeg-dev \
    libomp-dev \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*
# COPY relight/ relight/
RUN git clone https://github.com/cnr-isti-vclab/relight.git
RUN cd relight && \
    cmake -DCMAKE_CXX_FLAGS="-fsigned-char" . && \
    make relight-cli && \
    cp relight-cli/relight-cli /usr/local/bin

# ---- Runtime stage ----
# FROM debian:stable-slim
# # Install minimal requirements to run CLI
# RUN apt update && apt install -y \
#     libjpeg62-turbo \
#     libqt6gui6
# # Copy the CLI binary
# COPY --from=0 /relight/relight-cli/relight-cli /usr/local/bin/relight-cli

# ENTRYPOINT ["relight-cli"]

FROM python:3.10-slim
# Install runtime dependencies needed by relight-cli binary
RUN apt update && apt install -y \
    libjpeg62-turbo \
    libqt6gui6 \
    && rm -rf /var/lib/apt/lists/*

# Copy relight-cli from builder
COPY --from=builder /relight/relight-cli/relight-cli /usr/local/bin/relight-cli

# Copy your FastAPI app code
# WORKDIR /app
COPY ./app/ /app/

# Install FastAPI dependencies
RUN pip install fastapi uvicorn python-multipart python-slugify

# Expose port and run FastAPI
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]