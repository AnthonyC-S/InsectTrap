import Get_Classification

def test():
	image_path = '/home/pi/InsectTrap/InsectTrapProject/test_image.jpg'
	print('initializing...')
	driver = Get_Classification.initialize_driver(True)
	print('getting ID...')
	driver, results = Get_Classification.get_ID(image_path, driver, False)
	print(results)
	Get_Classification.quit_driver(driver)
	
test()