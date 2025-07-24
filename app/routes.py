from flask import render_template, request
from app import app
from app.cables import lookup_by_standard, lookup_by_specs, lookup_by_range , format_entry
from app.vlsm import (
    calculate_vlsm_requirements,
    assign_vlsm_blocks,
    ip_in_base_network,
    find_ip_subnet
)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/vlsm", methods=["GET", "POST"])
def vlsm():
    if request.method == "POST":
        try:
            # Extract form input
            base_network = request.form["base_network"].strip()  # e.g. 192.168.1.0/24
            host_counts = request.form["host_counts"].strip()     # e.g. 50, 20, 10
            target_ip = request.form.get("target_ip", "").strip() or None

            # Split base IP and CIDR
            base_ip, base_cidr = base_network.split('/')
            base_cidr = int(base_cidr)

            # Parse host list
            host_requirements = [int(h.strip()) for h in host_counts.split(',') if h.strip().isdigit()]

            # Run VLSM logic
            vlsm_blocks = calculate_vlsm_requirements(host_requirements)
            assignments = assign_vlsm_blocks(base_ip, base_cidr, vlsm_blocks)

            # Match IP if provided
            matched_block = None
            if target_ip and ip_in_base_network(target_ip, base_ip, base_cidr):
                matched_block = find_ip_subnet(target_ip, assignments)

            # Render output page
            return render_template("vlsm_result.html",
                                   assignments=assignments,
                                   target_ip=target_ip,
                                   matched_block=matched_block)
        except Exception as e:
            return f"<h3 style='color:red'>Error: {e}</h3>"

    return render_template("vlsm_form.html")

@app.route("/osi-model")
def iso_model():
    return render_template("osi_model.html")

@app.route("/osi-physical-layer")
def osi_physical_layer():
    return render_template("osi_physical_layer.html")

@app.route("/osi-data-link-layer")
def osi_data_link_layer(): 
    return render_template("osi_data_link_layer.html")

@app.route("/osi-network-layer")
def osi_network_layer():
    return render_template("osi_network_layer.html")    

@app.route("/osi-transport-layer")
def osi_transport_layer():
    return render_template("osi_transport_layer.html")

@app.route("/osi-session-layer")
def osi_session_layer():
    return render_template("osi_session_layer.html")

@app.route("/osi-presentation-layer")
def osi_presentation_layer():   
    return render_template("osi_presentation_layer.html")

@app.route("/osi-application-layer")
def osi_application_layer():
    return render_template("osi_application_layer.html")




@app.route("/cables", methods=["GET", "POST"])
def cables():
    result = None
    multiple = False
    error = None

    if request.method == "POST":
        standard = request.form.get("standard", "").strip()
        speed = request.form.get("speed", "").strip()
        medium = request.form.get("medium", "").strip()
        range_input = request.form.get("range", "").strip()
        range_medium = request.form.get("range_medium", "").strip()


        try:
            if standard:
                result = lookup_by_standard(standard)
                if not result:
                    error = f"No result found for standard: {standard}"
            elif speed and medium:
                result = lookup_by_specs(speed, medium)
                if not result:
                    error = f"No results found for {speed} over {medium}"
                elif isinstance(result, list):
                    multiple = True

            elif range_input:
                range_number = range_input
                result = lookup_by_range(range_number, range_medium)
                if not result:
                    error = f"No cables found supporting at least {range_number} meters."
                else:
                    multiple = True
            else:
                error = "Please enter either a standard or both speed and medium."
        except Exception as e:
            error = str(e)

    return render_template("cable_form.html", result=result, error=error, multiple=multiple)

@app.route("/what-is-a-route")
def what_is_a_routing():
    return render_template("what_is_routing.html")

@app.route("/what-is-a-routing-protocol")
def what_is_a_routing_protocol():
    return render_template("what_is_a_routing_protocol.html")

@app.route("/what-is-a-routing-tie")
def what_is_a_tie():
    return render_template("what_is_a_tie.html")

@app.route("/what-is-routing-time-interface")
def what_is_routing_time_interface():
    return render_template("what_is_routing_time_interface.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):   
    return render_template("500.html"), 500

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.png")