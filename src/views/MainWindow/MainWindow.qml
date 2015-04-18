import QtQuick 2.3
import QtQuick.Window 2.2
import QtGraphicalEffects 1.0
import QtQuick.Controls 1.0
import QtMultimedia 5.0
import DMusic 1.0
import "../DMusicWidgets"
import "../MusicManagerWindow"
import "../PlaylistManagerWindow"

Rectangle {

    id: mainWindow
    property var constants
    property var views: ['WebMusic360Page', 'MusicManagerPage', 'PlayListPage', 'DownloadPage']
    property var bgImage: bgImage
    property var titleBar: titleBar
    property var playBottomBar: playBottomBar
    property var webEngineViewPage: webEngineViewPage
    property var mainWindowController: mainWindowController
    property var temporaryLoader: temporaryLoader

    color: "white"
    focus: true

    BorderImage {
        id: bgImage
        objectName: 'bgImage'

        anchors.fill: mainWindow
        horizontalTileMode: BorderImage.Stretch
        verticalTileMode: BorderImage.Stretch
    }


    FastBlur {
        anchors.fill: bgImage
        source: bgImage
        // deviation: 4
        radius: 64
        // samples: 16
    }

    Column{

        Row{

            LeftSideBar {
                id: leftSideBar
                objectName: 'leftSideBar'
                width: 56
                height: mainWindow.height - playBottomBar.height
                iconWidth: leftSideBar.width
                iconHeight: leftSideBar.width
                color: "white"

                border.color: "lightgray"
                border.width: 1
            }

            Column{

                TitleBar {
                    id: titleBar
                    objectName: 'mainTitleBar'

                    width: mainWindow.width - leftSideBar.width
                    height: 25
                    iconWidth: titleBar.height
                    iconHeight: titleBar.height
                    color: "white"
                    windowFlag: true
                }

                DStackView {

                    id: stackViews
                    objectName: 'stackViews'
                    width: mainWindow.width - leftSideBar.width
                    height: mainWindow.height - titleBar.height - playBottomBar.height
                    currentIndex: 0

                    WebEngineViewPage {
                        id: webEngineViewPage

                        objectName: 'webEngineViewPage'

                        width: mainWindow.width - leftSideBar.width
                        height: mainWindow.height - titleBar.height - playBottomBar.height

                        url: ""
                        // Behavior on opacity {
                        //     NumberAnimation { duration: 500 }
                        // }
                    }

                    MusicManagerPage {
                        id: musicManagerPage
                        objectName: 'musicManagerPage'
                        anchors.fill: parent

                        // Behavior on opacity {
                        //     NumberAnimation { duration: 500 }
                        // }
                    }

                    PlaylistPage {
                        id: palylistPage

                        objectName: 'palylistPage'
                        anchors.fill: parent

                        // Behavior on opacity {
                        //     NumberAnimation { duration: 500 }
                        // }
                    }

                    DownloadPage {
                        id: downloadPage

                        objectName: 'downloadPage'
                        anchors.fill: parent

                        // Behavior on opacity {
                        //     NumberAnimation { duration: 500 }
                        // }
                    }
                }
            }
        }

        PlayBottomBar {
            id: playBottomBar
            width: mainWindow.width
            height: 90

            color: "#282F3F"
        }
    }

    MainWindowController{
        id: mainWindowController
        mainWindow: mainWindow
        bgImage: bgImage
        titleBar: titleBar
        leftSideBar: leftSideBar
        webEngineViewPage: webEngineViewPage
        playBottomBar: playBottomBar
    }

    Loader {
        id: temporaryLoader
        y: 150
        anchors.right: parent.right
        asynchronous: true
    }
}
