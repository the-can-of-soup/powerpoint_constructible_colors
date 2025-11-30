import common
import os

MAX_PRINTED_COLORS: int = 5000

if __name__ == '__main__':
    if os.path.isfile(common.CONSTRUCTIBLE_COLORS_FILE_PATH):
        print('Reading data...')

        with open(common.CONSTRUCTIBLE_COLORS_FILE_PATH, 'rb') as f:
            data: bytes = f.read()

        if len(data) % 3 == 0:
            print('Converting data...')

            constructible_colors: set[int] = set()
            for i in range(0, len(data), 3):
                color: tuple[int, int, int] = common.bytes_to_rgb(data[i:i+3])
                constructible_colors.add(common.rgb_to_decimal(color))
            constructible_count: int = len(constructible_colors)
            
            colors_to_be_printed: list[int] = []
            maybe_unconstructible_count: int = 0
            for decimal_color in range(1 << 24):
                if decimal_color not in constructible_colors:
                    if len(colors_to_be_printed) < MAX_PRINTED_COLORS:
                        colors_to_be_printed.append(decimal_color)
                    maybe_unconstructible_count += 1

            del constructible_colors

            print('')
            
            if maybe_unconstructible_count < 1:
                print('ALL COLORS ARE PROVEN CONSTRUCTIBLE!!!')
            else:
                print(f'{constructible_count} / {1 << 24} ({constructible_count / (1 << 24):.6%}) colors have been proven constructible.')
                print(f'{maybe_unconstructible_count} / {1 << 24} ({maybe_unconstructible_count / (1 << 24):.6%}) colors have not been proven constructible.')
                print('')
                if maybe_unconstructible_count <= MAX_PRINTED_COLORS:
                    input('Press ENTER to see all unproven colors.')
                    print('')
                    print('UNPROVEN COLORS')
                else:
                    input(f'Press ENTER to see the first {MAX_PRINTED_COLORS} unproven colors.')
                    print('')
                    print(f'FIRST {MAX_PRINTED_COLORS} UNPROVEN COLORS')

                print('')
                for decimal_color in colors_to_be_printed:
                    print(common.rgb_to_hex(common.decimal_to_rgb(decimal_color)))
        else:
            print('Corrupted data!')
    else:
        print('No data found.')

    print('')
    input('Press ENTER to close.')
