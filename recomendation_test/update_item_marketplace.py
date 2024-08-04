from update_item_marketplace_scr import update_item_marketplace,load_data_from_json
import argparse

def main(marketplace_name):
    data = load_data_from_json(marketplace_name)
    update_item_marketplace(data)
    print(f"Data has been successfully updated for {marketplace_name}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update marketplace items from JSON data.')
    parser.add_argument('marketplace_name', type=str, help='Marketplace name for which to update products')
    args = parser.parse_args()
    main(args.marketplace_name)
