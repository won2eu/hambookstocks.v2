# frontend build
FROM node:20-bookworm-slim AS frontend-build
WORKDIR /workspace/front-react

# Install yarn from distribution if not present; Node image includes corepack which provides yarn.
ENV PATH=/workspace/front-react/node_modules/.bin:$PATH
COPY front-react/package.json front-react/yarn.lock ./
# Use corepack to ensure deterministic yarn v1 behaviour (yarn.lock v1)
RUN corepack enable && corepack prepare yarn@1.22.19 --activate && \
    yarn install --frozen-lockfile --production=false

COPY front-react/ ./
RUN yarn build

# final image - Python FastAPI app
FROM python:3.12-slim-bookworm
# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Install runtime dependencies (keep to minimal recommended)
# No compilers installed; relying on prebuilt wheels from PyPI
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy frontend build artifacts into location expected by app
# React build outputs to /workspace/front-react/build
# The app mounts /front/assets and /front/vendor; put build static into front/assets and build root into front/vendor if appropriate
RUN mkdir -p front/assets front/vendor && \
    cp -r /workspace/front-react/build/static front/assets/ 2>/dev/null || true && \
    cp -r /workspace/front-react/build/* front/vendor/ 2>/dev/null || true

# Ensure non-root ownership
RUN chown -R appuser:appuser /app

USER appuser

# Expose the port used by uvicorn in main
EXPOSE 8000

# Run the app with uvicorn, bound to 0.0.0.0
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
