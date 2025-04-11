from new_invoice import add_new_invoice
from encryption import Encryption
from data_manager import DataManager

def handle_invoice(mode: str, target_id: int = None):

    key = "AbascuS@800144!!"
    encryptor = Encryption(key)
    file_path = "data/data.parquet"
    data_manager = DataManager(file_path)

    if mode == "input":
        new_invoice = add_new_invoice()
        encrypted_invoice = encryptor.encrypt(new_invoice)
        new_id = data_manager.generate_new_id()
        data = {"id": new_id, "document": encrypted_invoice}
        data_manager.save_data(data)
        print("Data saved.")
    elif mode == "output":
        if target_id is None:
            raise ValueError("ID mora biti prosleđen za output mod.")
        df = data_manager.get_data()
        row = df[df["id"] == target_id]
        if row.empty:
            print(f"Nema zapisa sa ID = {target_id}")
            return
        encrypted_data = row.iloc[0]["document"]
        decrypted = encryptor.decrypt(encrypted_data)
        print("Dekriptovani podaci:", decrypted)
    else:
        raise ValueError("Mode mora biti 'input' ili 'output'")


### USAGE ###
# id = 1
# handle_invoice("input")  
# handle_invoice("output", id)  