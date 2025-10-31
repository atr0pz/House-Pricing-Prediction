from django.core.management.base import BaseCommand
import os
import joblib
import pandas as pd
import numpy as np

class Command(BaseCommand):
    help = "Train the house price model from housePrice.csv and save the best estimator."

    def add_arguments(self, parser):
        parser.add_argument('--csv', type=str, default='housePrice.csv', help='Path to CSV file')
        parser.add_argument('--out', type=str, default=None, help='Output model path (joblib)')

    def handle(self, *args, **options):
        csv_path = options['csv']
        out_path = options['out'] or os.environ.get('HOUSE_MODEL_PATH') or os.path.join(os.path.dirname(__file__), '..', '..', 'model.joblib')
        out_path = os.path.abspath(out_path)

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_path}'))
            return

        self.stdout.write(self.style.NOTICE('Loading CSV...'))
        df = pd.read_csv(csv_path)
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
                pass

        df['Area'] = pd.to_numeric(df['Area'], errors='coerce')
        df['Area'] = df['Area'].fillna(df['Area'].median())

        bin_cols = ['Room', 'Parking', 'Warehouse', 'Elevator']
        df[bin_cols] = df[bin_cols].fillna(df[bin_cols].mode().iloc[0])

        if 'Price' in df.columns:
            df = df.drop(columns=['Price'])
        df['Price(USD)'] = pd.to_numeric(df['Price(USD)'], errors='coerce')
        df['Price(USD)'] = df['Price(USD)'].fillna(df['Price(USD)'].median())
        df['Price(USD)'] = np.log1p(df['Price(USD)'])

        df['Address'] = df['Address'].fillna('Unknown').astype(str)

        X = df[['Area', 'Room', 'Parking', 'Warehouse', 'Elevator', 'Address']]
        y = df['Price(USD)']

        self.stdout.write(self.style.NOTICE('Starting grid search (this may take a while)...'))

        from sklearn.ensemble import RandomForestRegressor
        from sklearn.pipeline import Pipeline
        from sklearn.model_selection import GridSearchCV, KFold
        import category_encoders as ce

        pipeline = Pipeline([
            ('encoder', ce.TargetEncoder(cols=['Address'])),
            ('model', RandomForestRegressor(random_state=42))
        ])

        param_grid = {
            'model__n_estimators': [100, 200],
            'model__max_depth': [None, 10, 20],
            'model__min_samples_split': [2, 5],
            'model__min_samples_leaf': [1, 2]
        }

        cv = KFold(n_splits=5, shuffle=True, random_state=42)

        grid_search = GridSearchCV(
            estimator=pipeline,
            param_grid=param_grid,
            cv=cv,
            scoring='r2',
            n_jobs=-1,
            verbose=2
        )

        grid_search.fit(X, y)
        best = grid_search.best_estimator_
        self.stdout.write(self.style.SUCCESS(f'Best params: {grid_search.best_params_}'))
        best.fit(X, y)

        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        joblib.dump(best, out_path)
        self.stdout.write(self.style.SUCCESS(f'Model saved to {out_path}'))