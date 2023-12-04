import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode

def read_barcodes(frame):
    barcodes = decode(frame)
    for barcode in barcodes:
        # Extract barcode data
        barcode_data = barcode.data.decode('utf-8')
        print("Barcode Data:", barcode_data)

        # Draw a rectangle around the barcode
        rect_points = barcode.rectangle
        if len(rect_points) == 4:
            rect_points = [(point[0], point[1]) for point in rect_points]
            rect_points = tuple(map(tuple, rect_points))
            cv2.polylines(frame, [np.array(rect_points)], isClosed=True, color=(0, 255, 0), thickness=2)

            # Display the barcode data
            cv2.putText(frame, barcode_data, (rect_points[0][0], rect_points[0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error reading frame")
            break

        frame_with_barcodes = read_barcodes(frame)
        cv2.imshow('Live Barcode Reader', frame_with_barcodes)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
