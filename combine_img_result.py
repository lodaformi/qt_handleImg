import matplotlib.pyplot as plt
def vis_KP(im, pts):
    fig, ax = plt.subplots()
    ax.imshow(im,cmap='gray')
    ax.scatter(round(pts[0][0]), round(pts[0][1]), c='red')
    ax.scatter(round(pts[0][2]), round(pts[0][3]), c='green')
    ax.scatter(round(pts[0][4]), round(pts[0][5]), c='yellow')
    ax.scatter(round(pts[0][6]), round(pts[0][7]), c='white')
    ax.scatter(round(pts[0][8]), round(pts[0][9]), c='magenta')
    ax.scatter(round(pts[0][10]), round(pts[0][11]), c='cyan')
    plt.axis('on')
    plt.tight_layout()
    plt.draw()