# 필요한 모듈을 임포트
import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

# QMainWindow를 상속받은 그래프 창 클래스 정의
class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 창 설정
        self.setWindowTitle("PyQtGraph Example")  # 창의 제목 설정
        self.setGeometry(100, 100, 800, 600)  # 창의 위치와 크기 설정

        # 중앙 위젯 생성
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)  # QMainWindow의 중앙 위젯으로 설정

        # 레이아웃 생성 및 중앙 위젯에 설정
        layout = QVBoxLayout()  # 수직 레이아웃 생성
        self.central_widget.setLayout(layout)  # 중앙 위젯에 레이아웃 설정

        # 그래프 위젯 생성 및 레이아웃에 추가
        self.graph_widget = pg.PlotWidget()  # PyQtGraph의 PlotWidget 생성
        layout.addWidget(self.graph_widget)  # 레이아웃에 그래프 위젯 추가

        # 그래프 그리기
        self.plot_graph()  # 아래에서 정의한 메소드를 호출하여 그래프를 그림

    def plot_graph(self):
        # (1,1) 좌표에 점으로 그래프에 표시
        plot = self.graph_widget.plot([1], [1], pen=None, symbol='o')
        # 그래프 위젯에 (1,1) 좌표에 원 모양의 점을 표시하는 그래프 추가

# 메인 함수
def main():
    app = QApplication(sys.argv)  # PyQt5의 어플리케이션 생성
    window = GraphWindow()  # 위에서 정의한 그래프 창 클래스의 인스턴스 생성
    window.show()  # 그래프 창을 화면에 표시
    sys.exit(app.exec_())  # 어플리케이션 실행

# 스크립트가 직접 실행될 때만 main 함수 실행
if __name__ == "__main__":
    main()
