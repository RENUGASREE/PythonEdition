"""
Safety migration: Add the 'required_code_patterns' column to the challenges table
using IF NOT EXISTS (PostgreSQL only) so it is idempotent.
On SQLite the column is already handled by migration 0025.
"""
from django.db import migrations, connection


def add_column_if_missing(apps, schema_editor):
    vendor = connection.vendor
    if vendor == 'postgresql':
        schema_editor.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = 'challenges'
                    AND column_name = 'required_code_patterns'
                ) THEN
                    ALTER TABLE challenges
                    ADD COLUMN required_code_patterns jsonb NULL;
                END IF;
            END $$;
        """)
    # SQLite: 0025 already covers this; no action needed locally


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_challenge_required_code_patterns'),
    ]

    operations = [
        migrations.RunPython(add_column_if_missing, migrations.RunPython.noop),
    ]
