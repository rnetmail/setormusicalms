/** @type {import('next').NextConfig} */
const nextConfig = {
  // Esta opção é CRUCIAL para o build do Docker.
  // Ela cria uma pasta .next/standalone com o mínimo necessário para rodar.
  output: 'standalone',
};

module.exports = nextConfig;
