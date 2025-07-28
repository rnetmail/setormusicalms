/** @type {import('next').NextConfig} */
const nextConfig = {
  // Esta opção otimiza o build para Docker, criando uma pasta 'standalone'
  // com todas as dependências necessárias, resultando em imagens menores.
  output: 'standalone',
};

export default nextConfig;
