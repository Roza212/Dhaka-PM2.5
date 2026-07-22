import os
import torch
import mlflow
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("Trainer")

def train():
    logger.info("Initializing MLflow tracking...")
    
    # MLflow Setup
    mlflow.set_experiment("Dhaka_PM25_STGCN")
    
    with mlflow.start_run() as run:
        logger.info(f"Started Run ID: {run.info.run_id}")
        
        # Log Training Hyperparameters
        hyperparams = {
            "learning_rate": 0.001,
            "epochs": 15,
            "batch_size": 32,
            "optimizer": "Adam",
            "model": "STGCN"
        }
        mlflow.log_params(hyperparams)
        
        # Simulated Training Loop
        logger.info("Starting training loop...")
        for epoch in range(hyperparams["epochs"]):
            # Simulating loss convergence
            train_loss = max(0.05, 1.2 - (epoch * 0.08))
            val_loss = max(0.08, 1.3 - (epoch * 0.07))
            
            # Log metrics per epoch
            mlflow.log_metric("train_loss", train_loss, step=epoch)
            mlflow.log_metric("val_loss", val_loss, step=epoch)
            
            if epoch % 5 == 0:
                logger.info(f"Epoch {epoch}/{hyperparams['epochs']} - Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
                
        # Save dummy model weights to be tracked by DVC
        model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, "stgcn_weights.pth")
        
        with open(model_path, "w") as f:
            f.write("mock_model_weights_tensor")
            
        logger.info(f"Model weights saved to {model_path}")
        mlflow.log_artifact(model_path)
        logger.info("Training complete.")

if __name__ == "__main__":
    train()
