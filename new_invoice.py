def add_new_invoice():
    komitent = input("Naziv komitenta: ")
    invoice_number = input("Broj fakture: ")
    date = input("Datum fakture (YYYY-MM-DD): ")
    invoice_value = input("Iznos fakture: ")
    note = input("Napomena: ")

    # new_entry = {
    #     'document': {
    #         'komitent': komitent,
    #         'date': date,
    #         'invoice_number': invoice_number,
    #         'invoice_value': invoice_value,
    #         'note': note
    #     }
    # }
    new_entry =  {
            'komitent': komitent,
            'date': date,
            'invoice_number': invoice_number,
            'invoice_value': invoice_value,
            'note': note
        }

    return new_entry


