import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Flag to avoid checking downloads repeatedly
_nltk_downloaded = False

def ensure_nltk_resources():
    """Ensure NLTK datasets are downloaded and available."""
    global _nltk_downloaded
    if not _nltk_downloaded:
        resources = ['punkt', 'stopwords', 'wordnet', 'omw-1.4']
        for res in resources:
            try:
                nltk.download(res, quiet=True)
            except Exception as e:
                print(f"Warning: Failed to download NLTK resource {res}: {e}")
        _nltk_downloaded = True

def preprocess_text(text: str) -> list:
    """
    Cleans and tokenizes raw text.
    Steps:
      1. Lowercase text.
      2. Remove punctuation.
      3. Tokenize.
      4. Remove stop words.
      5. Lemmatize.
    
    Args:
        text (str): Raw string of text.
        
    Returns:
        list: A list of clean, lemmatized tokens.
    """
    if not text:
        return []
        
    ensure_nltk_resources()
    
    # 1. Lowercase
    text = text.lower()
    
    # Replace newlines and multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # 2. Tokenize (retaining letters/numbers/plus/hash for skills like C++, C#)
    # We construct a custom token filter to keep track of programming-specific symbols
    tokens = word_tokenize(text)
    
    # 3. Stopword removal and cleaning
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    cleaned_tokens = []
    for token in tokens:
        # Strip simple punctuation except special symbols inside programming languages (like +, #)
        cleaned_token = token.strip(string.punctuation.replace('+', '').replace('#', ''))
        
        if cleaned_token and cleaned_token not in stop_words:
            # Lemmatize the token
            lemmatized = lemmatizer.lemmatize(cleaned_token)
            if lemmatized:
                cleaned_tokens.append(lemmatized)
                
    return cleaned_tokens

def get_normalized_text(text: str) -> str:
    """
    Preprocesses text and joins the tokens back into a space-separated string.
    
    Args:
        text (str): Raw string of text.
        
    Returns:
        str: Space-separated clean normalized tokens.
    """
    return " ".join(preprocess_text(text))
