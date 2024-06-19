#pragma once

#include <QTimer>

struct FSMNode
{
    int stateId;

    std::function<void()> entryAction;
    std::function<void()> exitAction;

    QMap<int, std::function<void()>> eventActions;

    QMap<int, int> transitions;
};

class FSMBase : public QObject
{
    Q_OBJECT

public:
    explicit FSMBase(QObject *parent = nullptr)
        : QObject(parent)
    {
    }

    int currentStateId() const
    {
        return _currentStateId;
    }

    void postEvent(int eventId)
    {
        QTimer::singleShot(0, this, [this, eventId] {
            _handleEvent(eventId);
        });
    }

signals:
    void currentStateIdChanged();
    void logOutput(QString log);

protected:
    virtual QString _eventIdString(int id) = 0;
    virtual QString _stateIdString(int id) = 0;

private:
    void _handleEvent(int eventId)
    {
        if (_fsmNodes[_currentStateId].eventActions.contains(eventId)) {
            _doEventAction(eventId);
        }
        _handleTransition(eventId);
    }

    void _handleTransition(int eventId)
    {
        if (_fsmNodes[_currentStateId].transitions.contains(eventId)) {
            _doExitAction();
            _goToState(_fsmNodes[_currentStateId].transitions[eventId], eventId);
        }
    }

    void _doEventAction(int eventId)
    {
        _fsmNodes[_currentStateId].eventActions[eventId]();
    }

    void _doEntryAction()
    {
        if (_fsmNodes[_currentStateId].entryAction)
            _fsmNodes[_currentStateId].entryAction();
    }

    void _doExitAction()
    {
        if (_fsmNodes[_currentStateId].exitAction)
            _fsmNodes[_currentStateId].exitAction();
    }

    void _goToState(int stateId, int eventId)
    {
        QString log = QString("%1 state from %2 to %3 by event %4")
                          .arg(_fsmName)
                          .arg(_stateIdString(_currentStateId))
                          .arg(_stateIdString(stateId))
                          .arg(_eventIdString(eventId));
        emit logOutput(log);

        _currentStateId = stateId;
        emit currentStateIdChanged();
        _doEntryAction();
    }

protected:
    QString             _fsmName;
    QMap<int, FSMNode>  _fsmNodes;
    int                 _currentStateId;
};
