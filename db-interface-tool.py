# import create_tables
import textwrap


def main():
    # setup tables
    setup_table = input("Drop all tables and re-create them (y/n): ")

    if setup_table.strip().lower() == "y":
        create_tables.recreate_tables()
    # add bin info
    add_bin = input("\nAdd bin to table (y/n): ")

    if add_bin.strip().lower() == "y":

        bin_info_help = """\n\
        GUIDE
        ----
        - ip_address <str>: 1 or more ip addresses for each internet connected microcontroller on a bin.
        - bin_height <int>: the height of the bin in cm.
        - location <str>: the name of the location of where the bin is located
        - bin_type <str>: a single character. R - Recycling, L - Landfill, C - Compost
        - waste_metrics <str>: a string of characters representing the metrics collected for the bin (eg. FP). F - fullness, P - Photo, W - Weight, and U - Usage
        ----
        """
        print(textwrap.dedent(bin_info_help))

        add_another = True

        while add_another:

            ip_address = input("ip_address: ")
            bin_height = input("bin_height: ")
            location = input("location: ")
            bin_type = input("bin_type: ")
            waste_metrics = input("waste_metrics: ")

            post_bin_info(
                ip_address, int(bin_height), location, bin_type, waste_metrics
            )

            add_query = input("\nAdd another bin (y/n)?: ")
            if add_query.strip().lower() != "y":
                add_another = False


# add bin_info
def post_bin_info(ip_address, bin_height, location, bin_type, waste_metrics):
    postRequest = {
        "data": [
            {
                "ip_address": "{}",
                "bin_height": {},
                "location": "{}",
                "bin_type": "{}",
                "waste_metrics": "{}",
            }
        ]
    }
    r = requests.post(
        BASEURL + "/bin-info", data=json.dumps(postRequest), headers=HEADERS
    )
    print(r.content)
    assert r.status_code == 201


#

if __name__ == "__main__":
    main()
