import ezdxf
from helper import chunks

def generate_dxf_horizontal_bands(circles, output_file_path, generation_parameters):
    print('generate horizontal band dxf...')
    doc,msp = _create_dxf_file()

    _plot_bounding_box(msp, generation_parameters)

    radius_weight_x = 0.5
    radius_weight_y = 1

    points = [((center[0] + radius * radius_weight_x, center[1] + radius * radius_weight_y), (center[0] - radius * radius_weight_x, center[1] - radius * radius_weight_y)) for (center, radius) in circles]
    point_rows = chunks(points, generation_parameters.target_width)
    for point_row in point_rows:
        pairs = zip(point_row[0:-1], point_row[1:])
        for pair in pairs:
            msp.add_line(pair[0][0], pair[1][0])
            msp.add_line(pair[0][1], pair[1][1])

        first_pair = point_row[0]
        last_pair = point_row[-1]
        width = generation_parameters.target_width * generation_parameters.mm_per_pixel
        msp.add_line((0, first_pair[0][1]), first_pair[0])
        msp.add_line((0, first_pair[1][1]), first_pair[1])
        msp.add_line((0, first_pair[0][1]), (0, first_pair[1][1]))
        msp.add_line(last_pair[0], (width, last_pair[0][1]))
        msp.add_line(last_pair[1], (width, last_pair[1][1]))
        msp.add_line((width, last_pair[0][1]), (width, last_pair[1][1]))
 
    print(f'write dxf to {output_file_path}')
    doc.saveas(output_file_path)

def generate_dxf_circles(circles, output_file_path, generation_parameters):
    doc,msp = _create_dxf_file()

    _plot_bounding_box(msp, generation_parameters)
    
    print(f' - draw {generation_parameters.target_width * generation_parameters.target_height} circles with {generation_parameters.mm_per_pixel} mm per pixel')

    for circle in circles:
        (center, radius) = circle
        msp.add_circle(center, radius)
        
    print(f'write dxf to {output_file_path}')
    doc.saveas(output_file_path)

def generate_dxf_stick_circles(sticks, output_file_path, generation_parameters):
    doc,msp = _create_dxf_file()

    _plot_bounding_box(msp, generation_parameters)
    
    print(f' - draw {generation_parameters.target_width * generation_parameters.target_height} circles with {generation_parameters.mm_per_pixel} mm per pixel')

    for stick in sticks:
        (center, radius, _) = stick
        msp.add_circle(center, radius)
        
    print(f'write dxf to {output_file_path}')
    doc.saveas(output_file_path)

def write_stick_length_file(sticks, output_file_path):
    print(f'write stick lengths to {output_file_path}')
    with open(output_file_path, 'w+') as file: 
        for stick in sticks:
            (center, _, length) = stick
            file.write(f'{center[0]:3.0f}x{center[1]:3.0f} - {length:2.0f}\n')

def _create_dxf_file():
    print('writing dxf output...')
    doc = ezdxf.new(dxfversion='R2010')
    msp = doc.modelspace()

    return doc,msp

def _plot_bounding_box(msp, generation_parameters):
    print(' - draw outer box')
    width = generation_parameters.target_width * generation_parameters.mm_per_pixel + 2 * generation_parameters.margin_width
    height = generation_parameters.target_height * generation_parameters.mm_per_pixel + 2 * generation_parameters.margin_height
    msp.add_line((0,0), (width,0))
    msp.add_line((width,0), (width, height))
    msp.add_line((width,height), (0,height))
    msp.add_line((0, height), (0,0))

