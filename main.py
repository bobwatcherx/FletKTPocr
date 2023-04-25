from flet import *
import cv2
# INSTALL TESSERACT WITH apt install tesseract-ocr-i
import pytesseract


def main(page:Page):
	page.scroll ="auto"
	inputKtp = TextField(label="Insert YOu  ktp here")

	# AND AUTO FILL AFTER SUCCESS FIND TEXT IN IMAGE
	# AND I HAVE KTP IMAGE YOU CAN DOWNLOAD FROM GOOGLE
	con_result  = Container(
		padding=10,
		content=Column([
			Text("YOu Ktp Result",size=30),
			TextField(label="Provinsi"),
			TextField(label="Kabupaten"),
			TextField(label="NIK"),
			TextField(label="Name"),
			TextField(label="Gender"),
			TextField(label="Blood"),
			TextField(label="address"),
			TextField(label="kecamatan"),
			TextField(label="religion"),
			TextField(label="wedding"),
			TextField(label="jobs"),
			TextField(label="berlaku hingga"),

			])

		)

	def processfile(e):
		img = cv2.imread(inputKtp.value)
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		th,threshed = cv2.threshold(gray,127,255,cv2.THRESH_TRUNC)
		

		result = pytesseract.image_to_string(threshed)

		data={}

		# AND NOW FIND FIELD IN IMAGE KTP AND FILL
		# TO TEXTFIELD 
		for word in result.split("\n"):
			if "PROVINSI" in word:
				data['provinsi'] = ' '.join(word.split(" ")[-2:])
			elif "KABUPATEN" in word:
				data['kabupaten'] = word.split(" ")[-1]
			elif "NIK" in word:
				data['nik'] = word.split(" ")[-1]
			elif "Nama" in word:
				data['nama'] = ' '.join(word.split(" ")[1:])
			elif "Tempat/Tgl Lahir" in word:
				data['TempavTgiLahir'] = ' '.join(word.split(" ")[-3:])
			elif "Jenis Kelamin" in word:
				data['jenis_kelamin'] = word.split(" ")[2]
				data['gol_darah'] = word.split(" ")[-1]
			elif "Alamat" in word:
				data['alamat'] = result[result.index(word) + len(word):result.index(word)+ len(word) +26].strip()
			elif "Kel/Desa" in word:
				data['kelurahan'] = word.split(" ")[-1]
			elif "Kecamatan" in word:
				data['kecamatan'] = word.split(" ")[-1]
			elif "Agama" in word:
				data['agama'] = word.split(" ")[-1]
			elif "Status Perkawinan" in word:
				data['status_perkawinan'] = word.split(" ")[-1]
			elif "Pekerjaan" in word:
				data['pekerjaan'] = word.split(" ")[-1]
			elif "Berlaku Hingga" in word:
				data['berlaku_hingga'] = ' '.join(word.split(" ")[-2:])



		print(data)

		# AND NOW SET EACH TEXTFIELD FROM data
		if len(data) > 0:
			# THIS FOR Provinsi
			con_result.content.controls[1].value = data['provinsi']
			con_result.content.controls[2].value = data['kabupaten']
			con_result.content.controls[3].value = data['nik']
			con_result.content.controls[4].value = data['nama']
			con_result.content.controls[5].value = data['jenis_kelamin']
			con_result.content.controls[6].value = data['gol_darah']
			con_result.content.controls[7].value = data['alamat']
			con_result.content.controls[8].value = data['kecamatan']
			con_result.content.controls[9].value = data['agama']
			con_result.content.controls[10].value = data['status_perkawinan']
			con_result.content.controls[11].value = data['pekerjaan']
			con_result.content.controls[12].value = data['berlaku_hingga']

			# SHOW SNACKBAR IF SUCCESS 
			page.snack_bar = SnackBar(
				Text("success get data from KTP",size=30),
				bgcolor="green"
				)
			page.snack_bar.open = True

		page.update()


	page.add(
	Column([
		inputKtp,
		ElevatedButton("Process file",
		on_click=processfile
			),
		con_result, 

		])
		)

flet.app(target=main)
