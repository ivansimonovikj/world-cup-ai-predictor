import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from engineer_features import prepare_training_data

def train_predictor():
    # 1. Get the engineered data directly from your feature pipeline
    df = prepare_training_data()
    
    if df is None or len(df) == 0:
        print("No data available to train the model.")
        return

    print("\nPreparing data for scikit-learn...")

    # 2. Define our 7 Advanced Features (X) and Target (y)
    features = [
        'home_form_scored', 'home_form_conceded',
        'away_form_scored', 'away_form_conceded',
        'h2h_home_win_rate',
        'home_overall_strength', 'away_overall_strength'
    ]
    
    X = df[features]
    y = df['result'] # 0 = Away Win, 1 = Draw, 2 = Home Win

    # 3. Split into Training (80%) and Testing (20%) data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training on {len(X_train)} matches, testing on {len(X_test)} matches...\n")

    # 4. Initialize the AI Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # 5. Train the Random Forest
    print("Training the Random Forest algorithm...")
    model.fit(X_train, y_train)

    # 6. Make predictions on the hidden test set
    predictions = model.predict(X_test)

    # 7. Evaluate Performance
    accuracy = accuracy_score(y_test, predictions)
    print("\n==============================")
    print("        AI EVALUATION         ")
    print("==============================")
    print(f"Overall Accuracy: {accuracy * 100:.2f}%\n")
    
    print("Detailed Report:")
    print(classification_report(y_test, predictions, target_names=["Away Win", "Draw", "Home Win"]))

    # 8. Feature Importance (Looking inside the AI's Brain)
    print("\n==============================")
    print("      FEATURE IMPORTANCE      ")
    print("==============================")
    
    # Extract the importance scores and pair them with the column names
    importances = model.feature_importances_
    feature_ranking = pd.DataFrame({
        'Feature': features,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    
    # Print the ranked list
    print(feature_ranking.to_string(index=False))

if __name__ == "__main__":
    train_predictor()