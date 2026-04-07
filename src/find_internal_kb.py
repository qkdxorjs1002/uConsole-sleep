import os


def find_internal_kb(ids=["1eaf:0024", "feed:0000", "1eaf:0003"]):
    usb_device_path = ""

    for device in os.listdir("/sys/bus/usb/devices/"):
        device_path = os.path.join("/sys/bus/usb/devices", device)
        vendor_path = os.path.join(device_path, "idVendor")
        product_path = os.path.join(device_path, "idProduct")

        if os.path.isfile(vendor_path) and os.path.isfile(product_path):
            with open(vendor_path, "r") as f:
                vid = f.read().strip()

            with open(product_path, "r") as f:
                pid = f.read().strip()

            if f"{vid}:{pid}" in ids:
                usb_device_path = device_path
                break

    return usb_device_path


if __name__ == "__main__":
    print(find_internal_kb())
