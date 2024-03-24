import yaml
import ansible_runner


def load_and_print_inventory(inventory_path):
    with open(inventory_path, "r") as file:
        inventory = yaml.safe_load(file)

    print("Inventory Hosts and Groups:")
    # Iterate over all groups except '_meta'
    for group_name, group_vars in inventory.get("all", {}).get("children", {}).items():
        print(f"\nGroup: {group_name}")
        hosts = group_vars.get("hosts", {})
        for host, host_vars in hosts.items():
            print(f"  Host: {host}")
            ip_address = host_vars.get("ansible_host", "No IP Address")
            print(f"    IP Address: {ip_address}")
            print(f"    Port: {host_vars.get('ansible_port', 'No Port')}")
            print(f"    User: {host_vars.get('ansible_user', 'No User')}")


def run_ping_playbook(private_data_dir):
    r = ansible_runner.run(private_data_dir=private_data_dir, playbook="ping.yml")
    print("\nPing Results:")
    print(f"Status: {r.status}, Return Code: {r.rc}")
    print("Host Ping Results:")

    # Filter and print only successful ping results
    for event in r.events:
        if event["event"] == "runner_on_ok":
            host = event["event_data"].get("host", "Unknown")
            ping_response = event["event_data"].get("res", {}).get("ping")
            if ping_response:
                print(f"  {host}: {ping_response}")


def main():
    inventory_path = "./hosts.yml"  # Path to your inventory file
    # Path to your Ansible directory
    private_data_dir = "/workspaces/ensf400-lab5-ansible"

    # Load and print inventory details
    load_and_print_inventory(inventory_path)

    # If you decide to run the ping playbook, ensure 'ping.yml' is correctly set up
    run_ping_playbook(private_data_dir)


if __name__ == "__main__":
    main()
