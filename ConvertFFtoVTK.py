from FemFrameTool import *
# from grid import gu_build_from_net


def convert_fields(grid, path_field_p, path_field_u, path_field_s, path_save, path_field_hydro, path_field_h, dimension):
    # grid = gu_build_from_net(path_mesh)
    if path_field_p == '':
        p_field = ''
    else:
        p_field = read_fun(path_field_p)
    if path_field_u == '':
        u_field = ''
    else:
        u_field = read_vel(path_field_u)
    if path_field_s == '':
        s_field = ''
    else:
        s_field = read_fun(path_field_s)
    if path_field_hydro == '':
        hydro_field = ''
    else:
        hydro_field = read_fun(path_field_hydro)
    if path_field_h == '':
        h_field = ''
    else:
        h_field = read_fun(path_field_h)
    if dimension == 2:
        save_vtk_2d(path_save, grid, p_field, u_field, s_field, hydro_field, h_field)
    elif dimension == 3:
        save_vtk_3d(path_save, grid, p_field, u_field, s_field, hydro_field, h_field)


def convert_perm(grid, path_field_perm, path_save):
    if path_field_perm == '':
        pass
    else:
        perm_field = read_fun(path_field_perm)
        save_vtk_perm(path_save, grid, perm_field)


def convert_sl(path_sl, path_save):
    save_vtk_sl(path_sl, path_save)

# def convert_p(path_mesh, path_field_p, path_save):
#     grid = gu_build_from_net(path_mesh)
#     field = read_fun(path_field_p)
#     save_vtk(path_save, grid, field)
