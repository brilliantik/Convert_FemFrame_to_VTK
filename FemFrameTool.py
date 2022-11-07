# from typing import Tuple, List
import numpy as np
from numpy import ndarray


class SL:
	def __init__(self, st):
		# self.WellFrom = int(st[1])
		# self.WellTo = int(st[2])
		if int(st[1]) > int(st[2]):
			self.WellFrom = int(st[2])
			self.WellTo = int(st[1])
		elif int(st[1]) < int(st[2]):
			self.WellFrom = int(st[1])
			self.WellTo = int(st[2])
		self.Np = int(st[3])
		self.index = int(st[4])
		self.xy = None
		self.color = None
		self.FT = None


def read_net(path_mesh) -> tuple[ndarray, list[tuple[int, int, int]]]:
	ffile_mesh = open(path_mesh, 'r')
	file_mesh = ffile_mesh.readlines()
	ffile_mesh.close()
	n_nodes = int(file_mesh[0].split()[0])
	n_triangle = int(file_mesh[0].split()[1])
	vert = np.zeros((n_nodes, 2))
	for i in range(n_nodes):
		vert[i] = list(map(float, file_mesh[i + 1].split()[:2]))
	elem_vert: list[tuple[int, int, int]] = list()
	for i in range(n_triangle):
		elem_vert.append((
			int(file_mesh[i + 1 + n_nodes].split()[0]) - 1,
			int(file_mesh[i + 1 + n_nodes].split()[1]) - 1,
			int(file_mesh[i + 1 + n_nodes].split()[2]) - 1))
	return vert, elem_vert


def read_fun(path_file):
	ffile_field = open(path_file, 'r')
	file_field = ffile_field.readlines()
	ffile_field.close()
	field = [float(file_field[i].split()[0]) for i in range(len(file_field))]
	return field


def read_vel(path_file):
	ffile_field = open(path_file, 'r')
	file_field = ffile_field.readlines()
	ffile_field.close()
	field = [[float(file_field[i].split()[0]), float(file_field[i].split()[1])] for i in range(len(file_field))]
	return field


def save_vtk_3d(path_save, grid, data_p, data_u, data_s, data_hydro, data_h):
	file = open(path_save, 'w')
	file.writelines('# vtk DataFile Version 3.0')
	file.write('\n')
	file.write('Grid2D')
	file.write('\n')
	file.write('ASCII')
	file.write('\n')
	file.write('DATASET UNSTRUCTURED_GRID')
	file.write('\n')
	file.write('POINTS ' + str(grid.Nvert * 2) + ' double')
	file.write('\n')
	for i in range(grid.Nvert):
		file.write(str(grid.vert[i][0]) + ' ' + str(grid.vert[i][1]) + ' ' + '0')
		file.write('\n')
	for i in range(grid.Nvert):
		# file.write(str(grid.vert[i][0]) + ' ' + str(grid.vert[i][1]) + ' ' + '-0.1')
		file.write(str(grid.vert[i][0]) + ' ' + str(grid.vert[i][1]) + ' ' + str(-data_h[i]))
		file.write('\n')
	k = 0
	for i in range(grid.Nelem):
		k = k + grid.elem_nvert[i] * 2 + 1
	file.write('CELLS ' + str(grid.Nelem) + ' ' + str(k))
	file.write('\n')
	for i in range(grid.Nelem):
		s1 = str(grid.elem_nvert[i] * 2)
		s2 = []
		for j in range(grid.elem_nvert[i]):
			s1 = s1 + ' ' + str(grid.elem_vert[i][j])
			s2.append(grid.elem_vert[i][j] + grid.Nvert)
		# s2.reverse()
		s3 = ''
		for jj in range(len(s2)):
			s3 = s3 + ' ' + str(s2[jj])
		file.write(s1 + s3)
		file.write('\n')
	file.write('CELL_TYPES ' + str(grid.Nelem))
	file.write('\n')
	for i in range(grid.Nelem):
		file.write('13')
		file.write('\n')
	if data_p != '' or data_s != '' or data_hydro != '' or data_h != '':
		file.write('POINT_DATA ' + str(grid.Nvert * 2))
		file.write('\n')
	if data_p != '':
		file.write('SCALARS P double 1')
		file.write('\n')
		file.write('LOOKUP_TABLE default')
		file.write('\n')
		for i in range(grid.Nvert):
			file.write(str(data_p[i]))
			file.write('\n')
		for i in range(grid.Nvert):
			file.write(str(data_p[i]))
			file.write('\n')
	if data_s != '':
		file.write('SCALARS S double 1')
		file.write('\n')
		file.write('LOOKUP_TABLE default')
		file.write('\n')
		for i in range(grid.Nvert):
			file.write(str(data_s[i]))
			file.write('\n')
		for i in range(grid.Nvert):
			file.write(str(data_s[i]))
			file.write('\n')
	if data_hydro != '':
		file.write('SCALARS hydroconductivity double 1')
		file.write('\n')
		file.write('LOOKUP_TABLE default')
		file.write('\n')
		for i in range(grid.Nvert):
			file.write(str(data_hydro[i]))
			file.write('\n')
		for i in range(grid.Nvert):
			file.write(str(data_hydro[i]))
			file.write('\n')
	if data_h != '':
		file.write('SCALARS height double 1')
		file.write('\n')
		file.write('LOOKUP_TABLE default')
		file.write('\n')
		for i in range(grid.Nvert):
			file.write(str(data_h[i]))
			file.write('\n')
		for i in range(grid.Nvert):
			file.write(str(data_h[i]))
			file.write('\n')

	if data_u != '':
		file.write('CELL_DATA ' + str(grid.Nelem))
		file.write('\n')

		file.write('VECTORS U double')
		file.write('\n')
		for i in range(grid.Nelem):
			file.write(str(data_u[i][0]) + ' ' + str(data_u[i][1]) + ' ' + '0')
			file.write('\n')
	file.close()


def save_vtk_2d(path_save, grid, data_p, data_u, data_s, data_hydro, data_h):
	file = open(path_save, 'w')
	file.writelines('# vtk DataFile Version 3.0')
	file.write('\n')
	file.write('Grid2D')
	file.write('\n')
	file.write('ASCII')
	file.write('\n')
	file.write('DATASET UNSTRUCTURED_GRID')
	file.write('\n')
	file.write('POINTS ' + str(grid.Nvert) + ' double')
	file.write('\n')
	for i in range(grid.Nvert):
		file.write(str(grid.vert[i][0]) + ' ' + str(grid.vert[i][1]) + ' ' + '0')
		file.write('\n')
	k = 0
	for i in range(grid.Nelem):
		k = k + grid.elem_nvert[i] + 1
	file.write('CELLS ' + str(grid.Nelem) + ' ' + str(k))
	file.write('\n')
	for i in range(grid.Nelem):
		s = str(grid.elem_nvert[i])
		for j in range(grid.elem_nvert[i]):
			s = s + ' ' + str(grid.elem_vert[i][j])
		file.write(s)
		file.write('\n')
	file.write('CELL_TYPES ' + str(grid.Nelem))
	file.write('\n')
	for i in range(grid.Nelem):
		file.write('5')
		file.write('\n')
	if data_p != '' or data_s != '' or data_hydro != '' or data_h != '':
		file.write('POINT_DATA ' + str(grid.Nvert))
		file.write('\n')
	if data_p != '':
		file.write('SCALARS P double 1')
		file.write('\n')
		file.write('LOOKUP_TABLE default')
		file.write('\n')
		for i in range(grid.Nvert):
			file.write(str(data_p[i]))
			file.write('\n')
	if data_s != '':
		file.write('SCALARS S double 1')
		file.write('\n')
		file.write('LOOKUP_TABLE default')
		file.write('\n')
		for i in range(grid.Nvert):
			file.write(str(data_s[i]))
			file.write('\n')
	if data_hydro != '':
		file.write('SCALARS hydroconductivity double 1')
		file.write('\n')
		file.write('LOOKUP_TABLE default')
		file.write('\n')
		for i in range(grid.Nvert):
			file.write(str(data_hydro[i]))
			file.write('\n')
	if data_h != '':
		file.write('SCALARS height double 1')
		file.write('\n')
		file.write('LOOKUP_TABLE default')
		file.write('\n')
		for i in range(grid.Nvert):
			file.write(str(data_h[i]))
			file.write('\n')

	if data_u != '':
		file.write('CELL_DATA ' + str(grid.Nelem))
		file.write('\n')

		file.write('VECTORS U double')
		file.write('\n')
		for i in range(grid.Nelem):
			file.write(str(data_u[i][0]) + ' ' + str(data_u[i][1]) + ' ' + '0')
			file.write('\n')
	file.close()


def save_vtk_perm(path_save, grid, data_perm):
	file = open(path_save, 'w')
	file.writelines('# vtk DataFile Version 3.0')
	file.write('\n')
	file.write('Grid2D')
	file.write('\n')
	file.write('ASCII')
	file.write('\n')
	file.write('DATASET UNSTRUCTURED_GRID')
	file.write('\n')
	file.write('POINTS ' + str(grid.Nvert * 2) + ' double')
	file.write('\n')
	for i in range(grid.Nvert):
		file.write(str(grid.vert[i][0]) + ' ' + str(grid.vert[i][1]) + ' ' + '0')
		file.write('\n')
	for i in range(grid.Nvert):
		file.write(str(grid.vert[i][0]) + ' ' + str(grid.vert[i][1]) + ' ' + '-0.1')
		file.write('\n')
	k = 0
	for i in range(grid.Nelem):
		k = k + grid.elem_nvert[i] * 2 + 1
	file.write('CELLS ' + str(grid.Nelem) + ' ' + str(k))
	file.write('\n')
	for i in range(grid.Nelem):
		s1 = str(grid.elem_nvert[i] * 2)
		s2 = []
		for j in range(grid.elem_nvert[i]):
			s1 = s1 + ' ' + str(grid.elem_vert[i][j])
			s2.append(grid.elem_vert[i][j] + grid.Nvert)
		# s2.reverse()
		s3 = ''
		for jj in range(len(s2)):
			s3 = s3 + ' ' + str(s2[jj])
		file.write(s1 + s3)
		file.write('\n')
	file.write('CELL_TYPES ' + str(grid.Nelem))
	file.write('\n')
	for i in range(grid.Nelem):
		file.write('13')
		file.write('\n')
	if data_perm != '':
		file.write('POINT_DATA ' + str(grid.Nvert * 2))
		file.write('\n')
		file.write('SCALARS permeability double 1')
		file.write('\n')
		file.write('LOOKUP_TABLE default')
		file.write('\n')
		for i in range(grid.Nvert):
			file.write(str(data_perm[i]))
			file.write('\n')
		for i in range(grid.Nvert):
			file.write(str(data_perm[i]))
			file.write('\n')

	file.close()


def save_vtk_sl(path_sl, path_save):
	sl_file = open(path_sl, 'r').readlines()
	n_sl = int(sl_file[0].split()[0])

	sl_info = np.zeros(n_sl, dtype = SL)
	num = int(0)

	for i in range(n_sl):
		sl_file_input = sl_file[1 + num + i].split()
		sl = SL(sl_file_input)
		sl.xy = [
			(float(sl_file[2 + num + i + j].split()[0]),
				float(sl_file[2 + num + i + j].split()[1])) for j in range(sl.Np)]
		num += sl.Np
		sl.FT = [sl.WellFrom, sl.WellTo]
		sl_info[i] = sl

	file = open(path_save, 'w')
	file.writelines('# vtk DataFile Version 3.0')
	file.write('\n')
	file.write('StreamLines')
	file.write('\n')
	file.write('ASCII')
	file.write('\n')
	file.write('DATASET POLYDATA')
	file.write('\n')
	sum_np = 0

	for i in range(n_sl):
		sum_np = sum_np + sl_info[i].Np
	file.write('POINTS' + ' ' + str(sum_np) + ' ' + 'float')
	file.write('\n')
	points_str = ''

	for i in range(n_sl):
		for j in range(sl_info[i].Np):
			points_str = points_str + str(sl_info[i].xy[j][0]) + ' ' + str(sl_info[i].xy[j][1]) + ' ' + '0' + '\n'
	file.write(points_str)
	size_line = 0

	for i in range(n_sl):
		size_line = size_line + sl_info[i].Np + 1
	file.write('LINES' + ' ' + str(len(sl_info)) + ' ' + str(size_line))
	lines_str = ''
	file.write('\n')

	index = 0
	for i in range(n_sl):
		lines_str = lines_str + str(sl_info[i].Np)
		for j in range(sl_info[i].Np):
			lines_str = lines_str + ' ' + str(j + index) + ' '
		lines_str = lines_str + '\n'
		index = index + sl_info[i].Np
	file.write(lines_str)
	file.close()
