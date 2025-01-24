# Usa una imagen base oficial de Python como capa base
FROM python:3.11-slim as base

# Definir variables de entorno para minimizar prompts interactivos y mejorar eficiencia
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# --- Etapa 1: Instalar dependencias del sistema ---
FROM base as system-dependencies

# Define el directorio de trabajo
WORKDIR /app

# Actualiza los repositorios e instala herramientas esenciales
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    apt-transport-https \
    ca-certificates \
    curl \
    --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# --- Etapa 2: Instalar navegadores (Google Chrome y Microsoft Edge) ---
FROM system-dependencies as browsers

# Añadir claves de Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'

# Añadir claves de Microsoft Edge
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list'

# Instalar navegadores
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    microsoft-edge-stable \
    --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Verifica las versiones instaladas (opcional)
RUN google-chrome --version && microsoft-edge --version

# --- Etapa 3: Instalar dependencias de Python ---
FROM base as python-dependencies

# Define el directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias (requirements.txt) para instalarlo
COPY requirements.txt /app/requirements.txt

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# --- Etapa 4: Imagen final ---
FROM browsers as final

# Copiar dependencias de Python desde la etapa anterior
COPY --from=python-dependencies /usr/local/lib/python3.11 /usr/local/lib/python3.11

# Copiar la aplicación al contenedor
COPY . /app

# Definir el directorio de trabajo
WORKDIR /app

# Comando por defecto para ejecutar la aplicación
CMD ["python", "-m", "main"]
