package screens;


import workers.Worker;
import screens.panels.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

/**
 * The main game screen that displays the game board, player information, and handles game interactions.
 * Manages the game state, user input, and rendering of all game components.
 */
public class MainPage extends Screen implements ActionListener {
    private PlayerPanel playerPanel;
    private BoardDisplay boardDisplay;
    private GameController gameController;
    private JLabel messageLabel;
    private boolean gameUpdated = false;
    private BenevolencePanel benevolencePanel;

    /**
     * Constructs the main game screen with all game components.
     *
     * @param parent the parent container panel for navigation
     * @param layout the CardLayout manager for screen transitions
     */
    public MainPage(JPanel parent, CardLayout layout, GameController gameController) {
        super(parent, layout, gameController);
        super.setLayout(new BorderLayout());


        this.gameController = gameController;

        // Set up mouse listener for board interactions
        this.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (!gameController.getGame().gameOver()) {
                    gameController.handleUserInput(e.getX(), e.getY(), getSquareSize());
                    SwingUtilities.invokeLater(() -> repaint());
                }
                updateMainPanel();
            }
        });


        boardDisplay = new BoardDisplay(gameController.getGame().getPlayers(), gameController.getGame().getBoard(), this);
        int boardDisplayWidth = 2 * this.getWidth() / 3;
        boardDisplay.setPreferredSize(new Dimension(boardDisplayWidth, this.getHeight()));


        benevolencePanel = new BenevolencePanel(gameController, parent, layout, this);
        benevolencePanel.setPreferredSize(new Dimension(boardDisplayWidth, this.getHeight()));


        playerPanel = new PlayerPanel(gameController.getGame().getPlayers(), layout, parent, this);
        // int playerPanelWidth = this.getWidth() / 3;
        // playerPanel.setPreferredSize(new Dimension(playerPanelWidth, this.getHeight()));
        playerPanel.setPlayers(gameController.getGame().getPlayers());

        this.messageLabel = new JLabel(this.gameController.getStageMessage());
        this.messageLabel.setFont(new Font("Arial", Font.BOLD, 20));

        if (this.gameController.getGame().getLoser() != null){
            this.add(benevolencePanel, BorderLayout.CENTER);
        }
        else {
            this.add(boardDisplay, BorderLayout.CENTER);
        }

        this.add(playerPanel, BorderLayout.EAST);
        this.add(messageLabel, BorderLayout.PAGE_END);

        updateMainPanel();
        this.revalidate();
        this.repaint();
    }

    /**
     * Gets the identifier for this screen.
     *
     * @return the screen name as "Main"
     */
    @Override
    public String getPageName() {
        return "Main";
    }

    /**
     * Handles action events (currently used for navigation to finish screen).
     *
     * @param e the ActionEvent to process
     */
    @Override
    public void actionPerformed(ActionEvent e) {
        this.getCardLayout().show(this.getPanelParent(), "Finish");
    }

    /**
     * Gets the currently active worker for the turn.
     *
     * @return the Worker object currently taking action
     */
    public Worker getCurrentWorker() {
        return this.gameController.getGame().getTurnTracker().getCurWorker();
    }

    /**
     * Calculates the optimal size for board squares based on window dimensions.
     *
     * @return the size in pixels for each square
     */
    public int getSquareSize() {
        int rows = gameController.getGame().getBoard().getRows();
        int cols = gameController.getGame().getBoard().getCols();

        int height = this.getHeight();
        int width = 2 * this.getWidth() /3;

        int squareSize = height / rows;
        if (width / cols < squareSize) {
            squareSize = width / cols;
        }
        return 95 * squareSize / 100;
    }


    /**
     * Paints the game components and handles game over state.
     *
     * @param g the Graphics object used for painting
     */
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        if (!gameUpdated){
            this.playerPanel.setPlayers(gameController.getGame().getPlayers());
            this.boardDisplay.setBoard(gameController.getGame().getBoard());
            this.boardDisplay.setPlayers(gameController.getGame().getPlayers());
            if (!this.gameController.isDefaultGame()){
                gameUpdated = true;
            }
        }
    }

    public void updateMainPanel(){
        this.remove(boardDisplay);
        this.remove(benevolencePanel);

        if (this.gameController.getGame().gameOver()){
            if (this.gameController.getGame().getLoser() != null && this.gameController.benevolencePossible()) {
                benevolencePanel = new BenevolencePanel(gameController, getPanelParent(), getCardLayout(), this);
                this.add(benevolencePanel, BorderLayout.CENTER);
            } else {
                FinalPage finalPage = new FinalPage(getPanelParent(), getCardLayout(), gameController);
                getPanelParent().add(finalPage, "Final");
                getCardLayout().show(getPanelParent(), finalPage.getPageName());
            }
        }
        else {
            this.add(boardDisplay, BorderLayout.CENTER);
        }

        messageLabel.setText(gameController.getStageMessage());

        this.revalidate();
        this.repaint();
    }

    @Override
    public void doLayout() {
        super.doLayout();
        int width = this.getWidth();
        int height = this.getHeight();

        boardDisplay.setPreferredSize(new Dimension((2 * width) / 3, height));
        playerPanel.setPreferredSize(new Dimension(width / 3, height));
    }
}