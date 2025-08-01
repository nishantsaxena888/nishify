import sys
from infra.pioneer_wholesale_inc import model_generator, mock_generator

if __name__ == "__main__":
    client_name = sys.argv[2]  # e.g. pioneer_wholesale_inc
    print(f"🔄 Resetting code for client: {client_name}")

    mock_generator.generate_mocks()
    model_generator.generate_models()

    print("✅ Code generated.")
