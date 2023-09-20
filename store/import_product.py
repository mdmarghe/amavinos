import pandas as pd
from django.core.management.base import BaseCommand
from .models import Product

class Command(BaseCommand):
    help = 'Import products from Excel/CSV file'

    def add_arguments(self, parser):
        parser.add_argument('Products.xlsx', type=str, help='Path to the Excel/CSV file to import')

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            # Assicurati che il file abbia un'estensione .csv
            if not file_path.endswith('.csv'):
                raise ValueError('Il file deve essere in formato CSV.')

            # Leggi il file CSV usando pandas
            df = pd.read_csv(file_path)

            # Itera attraverso le righe del DataFrame e importa i dati nel database
            for index, row in df.iterrows():
                product = Product(
                    name=row['Name'],
                    description=row['Description'],
                    price=row['Price']
                )
                product.save()

            self.stdout.write(self.style.SUCCESS('Importazione completata con successo'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Errore durante l\'importazione: {str(e)}'))
