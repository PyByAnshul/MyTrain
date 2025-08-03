from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
import requests
def main(trian_number):
    headers = {
        'authority': 'www.railyatri.in',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.railyatri.in',
        'referer': 'https://www.railyatri.in/',
        'sec-ch-ua': '^\\^Not_A',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '^\\^Windows^\\^',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    data = {
    'train_number': trian_number,
    'pnr_formhomepage': 'true'
    }

    response = requests.post('https://www.railyatri.in/live-train-status', headers=headers, data=data,)
    url = response.url  # Replace with the actual URL
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    # edge_options.add_argument("--headless")
    # edge_options.add_argument("--disable-gpu")
    # edge_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Edge(options=edge_options)
    # Navigate to the URL
    driver.get(url)
    # Wait for the dynamic content to load (you may need to adjust the sleep duration)
    # time.sleep(5)
    # Extract the content you need
    # For example, printing the page source
    # #print(driver.page_source)
    tag=BeautifulSoup(driver.page_source,'html.parser')
    table=tag.find('div',{'id':'main-block'})
    table_next=table.find_next_sibling('div',{'class':'white-timeline-bg'})
    head="""<head>
        <meta charset="utf-8" />
        <title>
            Live Running Status of Train 19031()- RailYatri
        </title>


        <link href="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.css" rel="stylesheet" type="text/css" />
        <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet" />
        <link href="https://images.railyatri.in/assets/mobile/mobile_views-e60898560ba22165a7ca5a3460cdcdca180101359d13aae6c72b983010a157f1.css.gz" media="all" rel="stylesheet" />

        <style type="text/css">
            .clearfix {
                clear: both;
            }
            
            .desktp-view {
                width: 65%;
                margin: 0 auto;
                float: none;
            }
            
            body {
                margin: 0 auto;
                padding: 0;
                font-family: Roboto, Helvetica, sans-serif;
                overflow-x: hidden;
                max-width: 1285px;
                background: #eeeeee;
                -webkit-box-shadow: -1px 3px 5px 0px rgba(0, 0, 0, 0.13);
                -moz-box-shadow: -1px 3px 5px 0px rgba(0, 0, 0, 0.13);
                box-shadow: -1px 3px 5px 0px rgba(0, 0, 0, 0.13);
                color: #363636 !important;
            }
            
            #header-main.top-section {
                background: #1079d7;
                position: relative;
                z-index: 999;
            }
            
            #header-main .navbar {
                min-height: auto !important;
                margin: 0px !important;
            }
            
            #header-main .navbar-default .navbar-collapse,
            #header-main .navbar-default .navbar-form {
                border-color: #e7e7e7;
                background: transparent;
            }
            
            a:focus,
            a:hover {
                text-decoration: none;
            }
            
            #header-main .navbar-brand {
                height: auto !important;
                padding: 0px;
                margin: 3px 0px 3px -5px !important;
                font-size: 12px;
                color: #777;
            }
            
            #header-main .navbar-nav li.offers-menu {
                background: #ffd461;
                height: 100%;
            }
            
            #header-main .navbar-nav li.offers-menu a {
                color: #000;
                font-weight: 600;
            }
            
            #header-main .navbar-nav>li>a {
                padding: 11px 25px;
            }
            
            #header-main .navbar-nav li.offers-menu a img {
                width: 15px;
                margin-top: -5px;
                /*margin-bottom: 2px;*/
            }
            
            #header-main .navbar-default {
                background: none;
                border: none;
            }
            
            #header-main .popup-sendlink {
                background: #363636;
                display: none;
                position: absolute;
                top: 47px;
                padding: 10px;
                border: 4px solid transparent;
            }
            
            #header-main .popup-sendlink:after,
            #header-main .popup-sendlink:before {
                bottom: 100%;
                left: 31%;
                border: solid transparent;
                content: " ";
                height: 0;
                width: 0;
                position: absolute;
                pointer-events: none;
            }
            
            #header-main .popup-sendlink:after {
                border-color: rgba(54, 54, 54, 0);
                border-bottom-color: #363636;
                border-width: 6px;
                margin-left: -6px;
            }
            
            #header-main .popup-sendlink:before {
                border-color: rgba(0, 0, 0, 0);
                border-bottom-color: transparent;
                border-width: 12px;
                margin-left: -12px;
            }
            
            #header-main ul.header-sign-in {
                width: 100%;
                padding: 0px;
                margin: 0px;
                list-style-type: none;
                float: right;
            }
            
            #app-link-button:hover,
            .login-button:hover,
            .login-button:active,
            #app-link-button:active {
                color: #363636;
                text-decoration: none;
            }
            
            #app-link-button,
            .login-button {
                background: #68bb00;
                border-radius: 18px;
                padding: 5px 18px;
                font-size: 16px;
                float: right;
                margin: 12px 0px 12px 10px;
                color: #fff!important;
            }
            
            #header-main .login-button {
                background: none!important;
                border: solid 2px #a0a0a0;
                padding: 3px 18px;
                color: #868686!important;
            }
            
            #app-link-button:hover,
            .login-button:hover,
            .login-button:active,
            #app-link-button:active {
                color: #363636;
            }
            
            #header-main .social-media-icons {
                background: #fff;
                /* Old browsers */
            }
            
            #header-main .social-media-icons-mobile {
                background: #feffff;
                /* Old browsers */
                background: -moz-linear-gradient(top, #feffff 0%, #d8d8d8 100%);
                /* FF3.6-15 */
                background: -webkit-linear-gradient(top, #feffff 0%, #d8d8d8 100%);
                /* Chrome10-25,Safari5.1-6 */
                background: linear-gradient(to bottom, #feffff 0%, #d8d8d8 100%);
                /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
                filter: progid: DXImageTransform.Microsoft.gradient( startColorstr='#feffff', endColorstr='#d8d8d8', GradientType=0);
                /* IE6-9 */
            }
            
            #header-main .navbar-header {
                clear: both;
            }
            
            #header-main .navbar-toggle {
                background: #3e4452;
                border: none;
            }
            
            #bs-example-navbar-collapse-1 {
                border: none;
                margin: 0px;
                float: right;
                padding-right: 0;
                width: 100%;
            }
            
            #header-main .navbar-default .navbar-nav>li>a {
                color: #fff;
            }
            
            #header-main .navbar-nav li.offers-menu a {
                color: #fff;
                font-weight: 600;
            }
            
            #header-main .navbar-nav>li>a {
                color: #fff;
                font-weight: normal;
                font-size: 14px;
                padding: 11px 30px;
            }
            
            #header-main .navbar-nav {
                float: right;
            }
            
            #header-main .ry-web-logo {
                width: auto !important;
                margin-top: 10px;
            }
            
            #header-main .popover-content {
                padding: 10px 10px;
                margin: 0px;
            }
            
            #header-main .popover-content ul {
                padding: 0px;
                text-decoration: none;
                margin: 0px;
                list-style-type: none;
            }
            
            #header-main .menu-items-list>li>a {
                padding: 10px 14px;
                clear: both;
                font-weight: 400;
                line-height: 1.42857143;
                color: #333;
                white-space: nowrap;
            }
            
            #header-main .menu-items-list>li>img {
                padding: 10px 14px;
                clear: both;
                font-weight: 400;
                line-height: 1.42857143;
                color: #333;
                white-space: nowrap;
            }
            
            #header-main .mobile_input {
                border: solid 1px #c2c2c2;
                color: #363636;
                font-size: 13px;
                padding: 8px;
                float: left;
                border-right: 0px;
                margin-left: 10px;
            }
            
            #header-main .send_download_link {
                width: 70px;
                margin-right: 10px;
                background: #1079d7;
                border: 0px;
                color: #fff;
            }
            
            .dweb_marg {
                margin-top: 75px;
            }
            
            .mainDiv {
                float: left;
                width: 100%;
                background-color: #eee;
                margin-top: 13px!important;
            }
            
            #main-block,
            #lts-error-block {
                /*border: 1px solid #e5e5e5;*/
                background: #fff;
            }
            /* .sticky {
        width: 63.5%;
    } */
            
            .timeline-plus-minus img {
                top: 4px;
                right: 3px;
            }
            
            .timeline-plus-minus img.minus-icon {
                top: 6px;
                right: 3px;
            }
            
            .lts-timeline_title h1 {
                font-size: 16px;
            }
            
            .lts-timeline_time-table span {
                font-size: 14px;
            }
            
            .lts-timeline_title .lts-timeline_time-table a {
                font-size: 14px;
            }
            
            #header-main .nav>li>a:hover {
                border-bottom: 0;
            }
            
            .top-section .social-media-icons {
                border-bottom: solid 0px #1079d7;
            }
            
            .sticky {
                width: 64.4%;
            }
            
            #right-ad_block {
                /*padding-top: 30px;
        padding-bottom: 30px;*/
            }
            
            #lts-error-block .timeline-listing .day_count,
            #next-stn-list .day_count {
                width: 26%;
            }
            
            .timeline-border-btn {
                width: 76.6%;
            }
            
            .marg-top-15 {
                box-shadow: none;
            }
            
            .right-side-wigd .dlts-prefill-block {
                border-radius: 6px;
                padding: 15px;
            }
            
            .right-side-wigd form input.form-control {
                width: 100%;
                height: 25px;
                background-color: #f2f2f2;
                color: #4a4a4a;
                border-top-right-radius: 0;
                border-bottom-right-radius: 0;
                border: 0;
                font-size: 12px;
            }
            
            .right-side-wigd form button {
                height: 25px;
                padding: 2px;
                border-top-left-radius: 0;
                border-bottom-left-radius: 0;
                border: 0;
                background-color: #4a90e2;
                color: #fff;
                font-size: 12px;
            }
            
            .ltsnetgps {
                display: none;
            }
            
            .dylts-stat {
                margin-bottom: 15px;
            }
            
            .dlts-cards_block {
                position: relative;
            }
            
            .dlts-cards_content.lts-cards_hotel {
                position: absolute;
                top: 25px;
                right: 0;
                width: 140px;
                margin-right: 60px;
            }
            
            .dlts-cards_content.lts-cards_hotel h5 {
                color: #4a90e2;
            }
            
            .dlts-cards_content.lts-cards_food {
                position: absolute;
                top: 25px;
                right: 0;
                width: 140px;
                margin-right: 60px;
            }
            
            .dlts-cards_content.lts-cards_food h5 {
                color: #fb674f;
            }
            
            .dlts-cards_content.lts-cards_train {
                position: absolute;
                top: 10px;
                right: 0;
                width: 140px;
                margin-right: 69px;
            }
            
            .dlts-cards_content.lts-cards_train h5 {
                color: #df5f6f;
            }
            
            .dlts-cards_content p {
                font-size: 14px;
                line-height: 1.2;
                color: #5d595f;
            }
            
            .modal-backdrop.in {
                z-index: 999 !important;
            }
            
            .menu-items-list {
                margin: 0px;
                list-style: none;
            }
            
            .mobOffers {
                width: 15px;
                height: 15px;
                margin: 0 -10px 0 0;
            }
            
            .top-nav-block {
                background: #fff;
            }
        </style>
    </head>"""
    table=head+str(table)+str(table_next)
    # Close the WebDriver
    driver.quit()
    return table