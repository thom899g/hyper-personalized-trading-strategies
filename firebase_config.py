"""
Firebase configuration and Firestore client initialization.
Uses Firebase Admin SDK for secure server-side access.
"""
import os
import logging
from typing import Optional
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.exceptions import FirebaseError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FirebaseManager:
    """Singleton manager for Firebase Firestore client"""
    
    _instance: Optional['FirebaseManager'] = None
    _db: Optional[firestore.Client] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseManager, cls).__new__(cls)
            cls._instance._initialize_firebase()
        return cls._instance
    
    def _initialize_firebase(self) -> None:
        """Initialize Firebase Admin SDK with error handling"""
        try:
            # Check for credentials in environment variable
            cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
            
            if cred_path and os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                logger.info(f"Loading Firebase credentials from: {cred_path}")
            elif 'FIREBASE_CONFIG' in os.environ:
                # Use environment configuration
                cred = credentials.ApplicationDefault()
                logger.info("Using application default credentials")
            else:
                raise ValueError(
                    "Firebase credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS "
                    "or FIREBASE_CONFIG environment variable."
                )
            
            # Initialize app if not already initialized
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            
            self._db = firestore.client()
            logger.info("Firebase Firestore client initialized successfully")
            
        except FirebaseError as e:
            logger.error(f"Firebase initialization error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during Firebase initialization: {str(e)}")
            raise
    
    @property
    def db(self) -> firestore.Client:
        """Get Firestore client instance"""
        if self._db is None:
            raise RuntimeError("Firebase not initialized. Call initialize() first.")
        return self._db
    
    def test_connection(self) -> bool:
        """Test Firestore connection by reading a test document"""
        try:
            # Try to read from a test collection
            test_ref = self.db.collection('connection_tests').document('test')
            test_ref.set({'timestamp': firestore.SERVER_TIMESTAMP}, merge=True)
            test_ref.get()
            logger.info("Firestore connection test successful")
            return True
        except Exception as e:
            logger.error(f"Firestore connection test failed: {str(e)}")
            return False

# Global instance for easy import
firebase_manager = FirebaseManager()