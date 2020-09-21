
import falcon

class print_x_real_ip(object):
    def process_request(self, req, resp):
        print(req.get_header('x-real-ip'))
