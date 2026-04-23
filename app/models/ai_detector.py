from app.services.stylometry_engine import extract_stylometric_features, ai_likelihood_from_features


class AIDetector:
    def predict(self, text: str) -> tuple[float, dict, list[str]]:
        features = extract_stylometric_features(text)
        score, explanations = ai_likelihood_from_features(features)
        return score, features, explanations
