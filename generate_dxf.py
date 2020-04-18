import ezdxf

def create_dxf_file():
    print('writing dxf output...')
    doc = ezdxf.new(dxfversion='R2010')
    msp = doc.modelspace()

    return doc,msp

def plot_bounding_box(msp, generation_parameters):
    print(' - draw outer box')
    msp.add_line((0,0), (generation_parameters.target_width * generation_parameters.mm_per_pixel,0))
    msp.add_line((generation_parameters.target_width * generation_parameters.mm_per_pixel,0), (generation_parameters.target_width * generation_parameters.mm_per_pixel, generation_parameters.target_height * generation_parameters.mm_per_pixel))
    msp.add_line((generation_parameters.target_width * generation_parameters.mm_per_pixel,generation_parameters.target_height * generation_parameters.mm_per_pixel), (0,generation_parameters.target_height * generation_parameters.mm_per_pixel))
    msp.add_line((0, generation_parameters.target_height * generation_parameters.mm_per_pixel), (0,0))

def generate_dxf_horizontal_bands(circles, output_file_path, generation_parameters):
    print('generate horizontal band dxf...')
    doc,msp = create_dxf_file()

    plot_bounding_box(msp, generation_parameters)

    print(f'write dxf to {output_file_path}')
    doc.saveas(output_file_path)

def generate_dxf_circles(circles, output_file_path, generation_parameters):
    doc,msp = create_dxf_file()

    plot_bounding_box(msp, generation_parameters)
    
    print(f' - draw {generation_parameters.target_width * generation_parameters.target_height} circles with {generation_parameters.mm_per_pixel} mm per pixel')

    for circle in circles:
        (center, radius) = circle
        msp.add_circle(center, radius)
        
    print(f'write dxf to {output_file_path}')
    doc.saveas(output_file_path)