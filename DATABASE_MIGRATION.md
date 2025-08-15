# Migração para PostgreSQL Exclusivo
## Documento de Migração - 12/08/2025

Este documento detalha as alterações realizadas para migrar o sistema Setor Musical MS para utilizar exclusivamente PostgreSQL como sistema de banco de dados, eliminando qualquer referência ou suporte a SQLite.

## Arquivos Atualizados

1. **config.py**:
   - Removidas configurações para SQLite
   - Configurado para usar exclusivamente a conexão PostgreSQL

2. **database.py**:
   - Removido código condicional para SQLite
   - Simplificado para usar apenas a conexão PostgreSQL

3. **docker-compose.yml**:
   - Removido volume `sqlite_data`
   - Removidas referências a SQLite nos comentários e volumes
   - Adicionadas variáveis de ambiente completas para PostgreSQL no serviço backend

4. **.env.example**:
   - Atualizado para incluir apenas configurações PostgreSQL
   - Adicionadas variáveis de ambiente detalhadas para conexão PostgreSQL

5. **.gitignore**:
   - Removidas entradas específicas para SQLite (*.db, *.sqlite3)
   - Removido comentário sobre arquivos de banco de dados SQLite

6. **README.md**:
   - Atualizado para refletir a configuração exclusiva de PostgreSQL
   - Adicionadas instruções específicas sobre persistência de dados
   - Incluídas recomendações para backups e atualizações seguras

## Benefícios da Migração

1. **Consistência de Dados**: Todas as operações agora usam um único sistema de banco de dados, evitando inconsistências.
2. **Escalabilidade**: PostgreSQL oferece melhor desempenho para crescimento futuro do sistema.
3. **Persistência Garantida**: O volume Docker dedicado assegura que os dados são preservados entre atualizações.
4. **Manutenção Simplificada**: Uma única tecnologia de banco de dados reduz a complexidade de manutenção.

## Procedimento de Migração de Dados

Para migrar dados existentes de uma instalação anterior que utilizava SQLite:

1. **Backup dos dados SQLite**:
   ```bash
   # Acesse o container backend
   docker exec -it setormusicalms-backend /bin/bash
   
   # Exporte os dados (se necessário)
   python -c "import sqlite3; conn = sqlite3.connect('data/database.sqlite3'); print('\n'.join([f'CREATE TABLE IF NOT EXISTS {t} AS SELECT * FROM {t};' for t in conn.execute('SELECT name FROM sqlite_master WHERE type=\"table\";').fetchall()]))" > migrate_tables.sql
   ```

2. **Importação para PostgreSQL**:
   ```bash
   # Execute os scripts SQL gerados no PostgreSQL
   docker exec -i setormusicalms-db psql -U mestre -d setormusicalms_db < migrate_tables.sql
   ```

3. **Verificação**:
   ```bash
   # Verifique se os dados foram importados corretamente
   docker exec -it setormusicalms-db psql -U mestre -d setormusicalms_db -c "\dt"
   ```

## Monitoramento e Backup

1. **Backup Diário Recomendado**:
   ```bash
   # Adicione ao crontab
   0 3 * * * docker exec setormusicalms-db pg_dump -U mestre setormusicalms_db > /path/to/backups/backup_$(date +\%Y\%m\%d).sql
   ```

2. **Monitoramento de Espaço em Disco**:
   ```bash
   # Verifique regularmente o uso do volume
   docker system df -v
   ```

## Confirmação da Migração

- [x] Removidas todas as referências a SQLite do código
- [x] Configuração do PostgreSQL verificada e testada
- [x] Docker Compose atualizado para usar apenas PostgreSQL
- [x] Documentação atualizada para refletir a nova configuração
- [x] Procedimentos de migração documentados