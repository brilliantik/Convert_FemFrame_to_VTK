import sys
# from PySide2.QtCore import *
# from PySide2.QtGui import *
# from PySide2.QtWidgets import *
import time
from threading import Thread
import multiprocessing
from PySide2 import QtCore, QtWidgets, QtGui
from gui import Ui_MainWindow
from ConvertFFtoVTK import convert_fields, convert_perm, convert_sl
from grid import gu_build_from_net

ui = Ui_MainWindow()

paths_p_field = ''
paths_u_field = ''
paths_s_field = ''
paths_SL = ''
paths_hydro_field = ''
paths_h_field = ''
n_p = -999999
n_u = -999999
n_s = -999999
n_SL = -999999
n_hydro = -999999
n_h = -999999
dimension = 2
type_hydro = 0
type_h = 0


def btb_path_net():
	filename = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QMainWindow(), 'Open file', '', "Image files (*.net)")
	ui.lineEdit_path_net.setText(filename[0])


def btb_path_hydroprovod():
	filename = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QMainWindow(), 'Open file', '', "Image files (*.fun)")
	ui.lineEdit_path_hydroprovod.setText(filename[0])


def btb_path_height():
	filename = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QMainWindow(), 'Open file', '', "Image files (*.fun)")
	ui.lineEdit_path_height.setText(filename[0])


def btb_paths_p_field():
	global paths_p_field, n_p
	filename = QtWidgets.QFileDialog.getOpenFileNames(QtWidgets.QMainWindow(), 'Open files', '', "Image files (*.fun)")
	paths_p_field = filename[0]
	n_p = len(filename[0])
	ui.lineEdit_paths_p_field.setText(str(n_p) + ' files selected')


def btb_paths_u_field():
	global paths_u_field, n_u
	filename = QtWidgets.QFileDialog.getOpenFileNames(QtWidgets.QMainWindow(), 'Open files', '', "Image files (*.vel)")
	paths_u_field = filename[0]
	n_u = len(filename[0])
	ui.lineEdit_paths_u_field.setText(str(n_u) + ' files selected')


def btb_paths_s_field():
	global paths_s_field, n_s
	filename = QtWidgets.QFileDialog.getOpenFileNames(QtWidgets.QMainWindow(), 'Open files', '', "Image files (*.fun)")
	paths_s_field = filename[0]
	n_s = len(filename[0])
	ui.lineEdit_paths_s_field.setText(str(n_s) + ' files selected')


def btb_paths_hydro_field():
	global paths_hydro_field, n_hydro
	filename = QtWidgets.QFileDialog.getOpenFileNames(QtWidgets.QMainWindow(), 'Open files', '', "Image files (*.fun)")
	paths_hydro_field = filename[0]
	n_hydro = len(filename[0])
	ui.lineEdit_paths_hydroprovod_field.setText(str(n_hydro) + ' files selected')


def btb_paths_h_field():
	global paths_h_field, n_h
	filename = QtWidgets.QFileDialog.getOpenFileNames(QtWidgets.QMainWindow(), 'Open files', '', "Image files (*.fun)")
	paths_h_field = filename[0]
	n_h = len(filename[0])
	ui.lineEdit_paths_height_field.setText(str(n_h) + ' files selected')


def btb_paths_save():
	filename = QtWidgets.QFileDialog.getExistingDirectory(QtWidgets.QMainWindow(), 'Open files', '')
	ui.lineEdit_paths_save.setText(filename)


# def btn_multi_convert():
# 	n = ui.spinBox_n_files.value()
# 	if n_p == -999999:
# 		pass
# 	elif n_p != n:
# 		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error",
# 									   "Кол-во полей давления не соответсвует \n введенному значению кол-ва vtk файлов!")
# 	if n_u == -999999:
# 		pass
# 	elif n_u != n:
# 		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error",
# 									   "Кол-во полей скорости не соответсвует \n введенному значению кол-ва vtk файлов!")
# 	if n_s == -999999:
# 		pass
# 	elif n_s != n:
# 		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error",
# 									   "Кол-во полей водонасыщенности не соответсвует "
# 									   "\n введенному значению кол-ва vtk файлов!")
# 	path_mesh = ui.lineEdit_path_net.text()
# 	if path_mesh == '':
# 		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error", "Не указан путь к файлу сетки!")
# 	else:
# 		path_folder_save = ui.lineEdit_paths_save.text()
# 		if path_folder_save == '':
# 			QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error", "Не указан путь сохранения файлов")
# 		else:
# 			t = time.time()
# 			grid = gu_build_from_net(path_mesh)
# 			path_hydroprovod = ui.lineEdit_path_hydroprovod.text()
# 			convert_perm(grid, path_hydroprovod, path_folder_save + '/perm.vtk')
# 			for i in range(n):
# 				path_save = path_folder_save + '/info_' + str(i) + '.vtk'
# 				if paths_p_field == '':
# 					path_p_field = ''
# 				else:
# 					path_p_field = paths_p_field[i]
# 				if paths_u_field == '':
# 					path_u_field = ''
# 				else:
# 					path_u_field = paths_u_field[i]
# 				if paths_s_field == '':
# 					path_s_field = ''
# 				else:
# 					path_s_field = paths_s_field[i]
# 				convert_p_u(grid, path_p_field, path_u_field, path_s_field, path_save)
# 				ui.progressBar.setValue(i * 100.0 / (n - 1))
# 			print(time.time() - t)


# Многопроцессорная конвертация
def btn_multi_convert_n_pr():
	n = ui.spinBox_n_files.value()

	if n_p == -999999:
		pass
	elif n_p == 0:
		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error",
									   "Поля давления не выбраны!")
	elif n_p != n:
		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error",
									   "Кол-во полей давления не соответсвует \n введенному значению кол-ва vtk файлов!")
	if n_u == -999999:
		pass
	elif n_u == 0:
		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error",
									   "Поля скоростей не выбраны!")
	elif n_u != n:
		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error",
									   "Кол-во полей скорости не соответсвует \n введенному значению кол-ва vtk файлов!")
	if n_s == -999999:
		pass
	elif n_s == 0:
		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error",
									   "Поля водонасыщенности не выбраны!")
	elif n_s != n:
		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error",
									   "Кол-во полей водонасыщенности не соответсвует "
									   "\n введенному значению кол-ва vtk файлов!")
	if n_hydro == -999999:
		pass
	elif n_hydro == 0:
		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error",
									   "Поля гидропроводности не выбраны!")
	elif n_hydro != n:
		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error",
									   "Кол-во полей гидропроводности не соответсвует "
									   "\n введенному значению кол-ва vtk файлов!")
	if n_h == -999999:
		pass
	elif n_h == 0:
		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error",
									   "Поля толщины не выбраны!")
	elif n_h != n:
		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error",
									   "Кол-во полей толщины не соответсвует "
									   "\n введенному значению кол-ва vtk файлов!")
	path_mesh = ui.lineEdit_path_net.text()
	if path_mesh == '':
		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error", "Не указан путь к файлу сетки!")
	else:
		path_folder_save = ui.lineEdit_paths_save.text()
		if path_folder_save == '':
			QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error", "Не указан путь сохранения файлов")
		else:
			t = time.time()
			grid = gu_build_from_net(path_mesh)
			arguments = []
			path_hydroprovod = ui.lineEdit_path_hydroprovod.text()
			path_h = ui.lineEdit_path_height.text()
			# if type_hydro == 0:
			# 	global paths_hydro_field
			# 	paths_hydro_field = [path_hydroprovod for i in range(n)]
			# elif type_hydro == 1:
			# 	paths = [paths_hydro_field[i] for i in range(n)]

			convert_perm(grid, path_hydroprovod, path_folder_save + '/perm.vtk')
			for i in range(n):
				path_save = path_folder_save + '/info_' + str(i) + '.vtk'
				if paths_p_field == '' or not ui.checkBox_paths_p_field.isChecked():
					path_p_field = ''
				else:
					path_p_field = paths_p_field[i]
				if paths_u_field == '' or not ui.checkBox_paths_u_field.isChecked():
					path_u_field = ''
				else:
					path_u_field = paths_u_field[i]
				if paths_s_field == '' or not ui.checkBox_paths_s_field.isChecked():
					path_s_field = ''
				else:
					path_s_field = paths_s_field[i]
				if paths_hydro_field == '' or not ui.checkBox_paths_hydroprovod_field.isChecked():
					path_hydro_field = ''
				else:
					path_hydro_field = paths_hydro_field[i]
				if paths_h_field == '' or not ui.checkBox_paths_height_field.isChecked():
					path_h_field = ''
				else:
					path_h_field = paths_h_field[i]
				if type_hydro == 0:
					path_hydro_field = path_hydroprovod
				if type_h == 0:
					path_h_field = path_h
				arguments.append((grid, path_p_field, path_u_field, path_s_field, path_save, path_hydro_field, path_h_field, dimension))
			# convert_p_u(grid, path_p_field, path_u_field, path_s_field, path_save)
			# th = Thread(target = convert_p_u, args=(grid, path_p_field, path_u_field, path_s_field, path_save,))
			# th.start()
			# ui.progressBar.setValue(i * 100.0 / (n - 1))
			with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
				p.starmap(convert_fields, arguments)
			p.join()
			ui.progressBar.setValue(100)
			print(time.time() - t)


def chk_paths_p_field():
	if ui.checkBox_paths_p_field.isChecked():
		ui.toolButton_paths_p_field.setEnabled(True)
		ui.toolButton_paths_save.setEnabled(True)
		ui.lineEdit_paths_save.setEnabled(True)
		ui.btn_multi_convert.setEnabled(True)
	elif not ui.checkBox_paths_p_field.isChecked() and not ui.checkBox_paths_u_field.isChecked() and not ui.checkBox_paths_s_field.isChecked() and not ui.checkBox_paths_hydroprovod_field.isChecked() and not ui.checkBox_paths_height_field.isChecked():
		ui.toolButton_paths_save.setEnabled(False)
		ui.lineEdit_paths_save.setEnabled(False)
		ui.btn_multi_convert.setEnabled(False)
	if not ui.checkBox_paths_p_field.isChecked():
		ui.toolButton_paths_p_field.setEnabled(False)


def chk_paths_u_field():
	if ui.checkBox_paths_u_field.isChecked():
		ui.toolButton_paths_u_field.setEnabled(True)
		ui.toolButton_paths_save.setEnabled(True)
		ui.lineEdit_paths_save.setEnabled(True)
		ui.btn_multi_convert.setEnabled(True)
	elif not ui.checkBox_paths_p_field.isChecked() and not ui.checkBox_paths_u_field.isChecked() and not ui.checkBox_paths_s_field.isChecked() and not ui.checkBox_paths_hydroprovod_field.isChecked() and not ui.checkBox_paths_height_field.isChecked():
		ui.toolButton_paths_save.setEnabled(False)
		ui.lineEdit_paths_save.setEnabled(False)
		ui.btn_multi_convert.setEnabled(False)
	if not ui.checkBox_paths_u_field.isChecked():
		ui.toolButton_paths_u_field.setEnabled(False)


def chk_paths_s_field():
	if ui.checkBox_paths_s_field.isChecked():
		ui.toolButton_paths_s_field.setEnabled(True)
		ui.toolButton_paths_save.setEnabled(True)
		ui.lineEdit_paths_save.setEnabled(True)
		ui.btn_multi_convert.setEnabled(True)
	elif not ui.checkBox_paths_p_field.isChecked() and not ui.checkBox_paths_u_field.isChecked() and not ui.checkBox_paths_s_field.isChecked() and not ui.checkBox_paths_hydroprovod_field.isChecked() and not ui.checkBox_paths_height_field.isChecked():
		ui.toolButton_paths_save.setEnabled(False)
		ui.lineEdit_paths_save.setEnabled(False)
		ui.btn_multi_convert.setEnabled(False)
	if not ui.checkBox_paths_s_field.isChecked():
		ui.toolButton_paths_s_field.setEnabled(False)


def chk_paths_hydro_field():
	if ui.checkBox_paths_hydroprovod_field.isChecked():
		ui.toolButton_paths_hydroprovod_field.setEnabled(True)
		ui.toolButton_paths_save.setEnabled(True)
		ui.lineEdit_paths_save.setEnabled(True)
		ui.btn_multi_convert.setEnabled(True)
	elif not ui.checkBox_paths_p_field.isChecked() and not ui.checkBox_paths_u_field.isChecked() and not ui.checkBox_paths_s_field.isChecked() and not ui.checkBox_paths_hydroprovod_field.isChecked() and not ui.checkBox_paths_height_field.isChecked():
		ui.toolButton_paths_save.setEnabled(False)
		ui.lineEdit_paths_save.setEnabled(False)
		ui.btn_multi_convert.setEnabled(False)
	if not ui.checkBox_paths_hydroprovod_field.isChecked():
		ui.toolButton_paths_hydroprovod_field.setEnabled(False)


def chk_paths_h_field():
	if ui.checkBox_paths_height_field.isChecked():
		ui.toolButton_paths_height_field.setEnabled(True)
		ui.toolButton_paths_save.setEnabled(True)
		ui.lineEdit_paths_save.setEnabled(True)
		ui.btn_multi_convert.setEnabled(True)
	elif not ui.checkBox_paths_p_field.isChecked() and not ui.checkBox_paths_u_field.isChecked() and not ui.checkBox_paths_s_field.isChecked() and not ui.checkBox_paths_hydroprovod_field.isChecked() and not ui.checkBox_paths_height_field.isChecked():
		ui.toolButton_paths_save.setEnabled(False)
		ui.lineEdit_paths_save.setEnabled(False)
		ui.btn_multi_convert.setEnabled(False)
	if not ui.checkBox_paths_height_field.isChecked():
		ui.toolButton_paths_height_field.setEnabled(False)


def btb_paths_sl():
	global paths_SL, n_SL
	filename = QtWidgets.QFileDialog.getOpenFileNames(QtWidgets.QMainWindow(), 'Open files', 'SLs_',
													  "Image files (*.txt)")
	paths_SL = filename[0]
	n_SL = len(filename[0])
	ui.lineEdit_paths_SL.setText(str(n_SL) + ' files selected')
	if n_SL > 0:
		ui.btn_multi_convert_SL.setEnabled(True)
	else:
		ui.btn_multi_convert_SL.setEnabled(False)


def btb_paths_save_sl():
	filename = QtWidgets.QFileDialog.getExistingDirectory(QtWidgets.QMainWindow(), 'Open files', '')
	ui.lineEdit_paths_save_SL.setText(filename)


def btn_multi_convert_sl_n_pr():
	if ui.lineEdit_paths_save_SL.text() == '':
		QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Error",
									   "Не указан путь сохранения!")
	else:
		t = time.time()
		arguments = []
		for i in range(n_SL):
			arguments.append((paths_SL[i], ui.lineEdit_paths_save_SL.text() + '/SL_' + str(i) + '.vtk'))
		with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
			p.starmap(convert_sl, arguments)
		p.join()
		ui.progressBar_2.setValue(100)
		print(time.time() - t)


def btn_apply_settings():
	global dimension, type_hydro, type_h
	if ui.comboBox_dimension.currentIndex() == 0:
		dimension = 2
	elif ui.comboBox_dimension.currentIndex() == 1:
		dimension = 3
	if ui.comboBox_hydroprovod.currentIndex() == 0:
		type_hydro = 0
		ui.checkBox_paths_hydroprovod_field.setEnabled(False)
		ui.toolButton_paths_hydroprovod_field.setEnabled(False)
		ui.lineEdit_path_hydroprovod.setEnabled(True)
		ui.toolButton_path_hydroprovod.setEnabled(True)
	elif ui.comboBox_hydroprovod.currentIndex() == 1:
		type_hydro = 1
		ui.checkBox_paths_hydroprovod_field.setEnabled(True)
		ui.lineEdit_path_hydroprovod.setEnabled(False)
		ui.toolButton_path_hydroprovod.setEnabled(False)
		if ui.checkBox_paths_hydroprovod_field.isChecked():
			ui.toolButton_paths_hydroprovod_field.setEnabled(True)
	if ui.comboBox_height.currentIndex() == 0:
		type_h = 0
		ui.checkBox_paths_height_field.setEnabled(False)
		ui.toolButton_paths_height_field.setEnabled(False)
		ui.lineEdit_path_height.setEnabled(True)
		ui.toolButton_path_height.setEnabled(True)
	elif ui.comboBox_height.currentIndex() == 1:
		type_h = 1
		ui.checkBox_paths_height_field.setEnabled(True)
		ui.lineEdit_path_height.setEnabled(False)
		ui.toolButton_path_height.setEnabled(False)
		if ui.checkBox_paths_height_field.isChecked():
			ui.toolButton_paths_height_field.setEnabled(True)


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)

	MainWindow = QtWidgets.QMainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()

	ui.toolButton_path_net.clicked.connect(btb_path_net)
	ui.toolButton_path_hydroprovod.clicked.connect(btb_path_hydroprovod)

	ui.toolButton_paths_p_field.clicked.connect(btb_paths_p_field)
	ui.toolButton_paths_u_field.clicked.connect(btb_paths_u_field)
	ui.toolButton_paths_s_field.clicked.connect(btb_paths_s_field)
	ui.toolButton_paths_save.clicked.connect(btb_paths_save)
	ui.btn_multi_convert.clicked.connect(btn_multi_convert_n_pr)

	ui.checkBox_paths_p_field.clicked.connect(chk_paths_p_field)
	ui.checkBox_paths_u_field.clicked.connect(chk_paths_u_field)
	ui.checkBox_paths_s_field.clicked.connect(chk_paths_s_field)
	ui.checkBox_paths_hydroprovod_field.clicked.connect(chk_paths_hydro_field)
	ui.checkBox_paths_height_field.clicked.connect(chk_paths_h_field)

	ui.toolButton_paths_SL.clicked.connect(btb_paths_sl)
	ui.toolButton_paths_save_SL.clicked.connect(btb_paths_save_sl)
	ui.btn_multi_convert_SL.clicked.connect(btn_multi_convert_sl_n_pr)
	ui.toolButton_paths_hydroprovod_field.clicked.connect(btb_paths_hydro_field)
	ui.toolButton_paths_height_field.clicked.connect(btb_paths_h_field)
	ui.btn_apply_settings.clicked.connect(btn_apply_settings)
	ui.toolButton_path_height.clicked.connect(btb_path_height)
	sys.exit(app.exec_())
