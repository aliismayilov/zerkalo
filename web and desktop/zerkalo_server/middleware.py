import re

class MobileDetectionMiddleware(object):
    """
    Useful middleware to detect if the user is
    on a mobile device.
    """

    def process_request(self, request):
        # 1 - desktop, 2 - advanced mobile browsers (like iPhone), 3 - basic mobile browsers (all others)
        browser_level = 1;

        if request.META.has_key('HTTP_USER_AGENT'):
            user_agent = request.META['HTTP_USER_AGENT']
            
            # Test advanced mobile values.
            pattern_2 = "(phone|android|iemobile)"
            prog_2 = re.compile(pattern_2, re.IGNORECASE)
            match = prog_2.search(user_agent)
            
            if match:
                browser_level = 2;
                request.browser_level = browser_level
                return

            # Test common mobile values.
            pattern = "(up.browser|up.link|mmp|symbian|smartphone|midp|wap|windows ce|pda|mobile|mini|palm|netfront)"
            prog = re.compile(pattern, re.IGNORECASE)
            match = prog.search(user_agent)

            if match:
                browser_level = 3;
            else:
                # Nokia like test for WAP browsers.
                # http://www.developershome.com/wap/xhtmlmp/xhtml_mp_tutorial.asp?page=mimeTypesFileExtension

                if request.META.has_key('HTTP_ACCEPT'):
                    http_accept = request.META['HTTP_ACCEPT']

                    pattern = "application/vnd\.wap\.xhtml\+xml"
                    prog = re.compile(pattern, re.IGNORECASE)

                    match = prog.search(http_accept)

                    if match:
                        browser_level = 3

            if browser_level == 1:
                # Now we test the user_agent from a big list.
                user_agents_test = ("w3c ", "acs-", "alav", "alca", "amoi", "audi",
                                    "avan", "benq", "bird", "blac", "blaz", "brew",
                                    "cell", "cldc", "cmd-", "dang", "doco", "eric",
                                    "hipt", "inno", "ipaq", "java", "jigs", "kddi",
                                    "keji", "leno", "lg-c", "lg-d", "lg-g", "lge-",
                                    "maui", "maxo", "midp", "mits", "mmef", "mobi",
                                    "mot-", "moto", "mwbp", "nec-", "newt", "noki",
                                    "xda",  "palm", "pana", "pant", "phil", "play",
                                    "port", "prox", "qwap", "sage", "sams", "sany",
                                    "sch-", "sec-", "send", "seri", "sgh-", "shar",
                                    "sie-", "siem", "smal", "smar", "sony", "sph-",
                                    "symb", "t-mo", "teli", "tim-", "tosh", "tsm-",
                                    "upg1", "upsi", "vk-v", "voda", "wap-", "wapa",
                                    "wapi", "wapp", "wapr", "webc", "winw", "winw",
                                    "xda-",)

                test = user_agent[0:4].lower()
                if test in user_agents_test:
                    browser_level = 3

        request.browser_level = browser_level